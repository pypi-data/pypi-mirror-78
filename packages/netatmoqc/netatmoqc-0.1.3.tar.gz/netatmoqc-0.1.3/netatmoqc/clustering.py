#!/usr/bin/env python3
import numpy as np
import pandas as pd
from hdbscan import HDBSCAN, RobustSingleLinkage
from sklearn.cluster import DBSCAN, OPTICS
from sklearn import metrics
from sklearn.neighbors import LocalOutlierFactor
from numba import njit, prange
import time
import sys
import logging
import io
from functools import wraps

# Local imports
from .config_parser import UndefinedConfigValue
from .load_data import read_netatmo_data_for_dtg
from .metrics import calc_distance_matrix

logger = logging.getLogger(__name__)


def suspendlogging(func):
    """
    Adapted from: <https://stackoverflow.com/questions/7341064/
                   disable-logging-per-method-function>
    """

    @wraps(func)
    def inner(*args, **kwargs):
        previousloglevel = logger.getEffectiveLevel()
        try:
            logger.setLevel(logging.WARN)
            return func(*args, **kwargs)
        finally:
            logger.setLevel(previousloglevel)

    return inner


def get_weights_array(
    df,
    pairwise_diff_weights={},
    skip=["id", "time_utc"],
    default=1,
    default_geodist=1,
):
    """
    Takes a pandas dataframe and a {column_name:weight} dictionary
    and returns a numpy array of weights to be passed to the routine
    that calculates the distance matrix.

    The "skip" arg lists columns that will not enter the clustering
    and should therefore be skipped.

    If the weight for a non-skipped column of the input dataframe
    are not defined in pairwise_diff_weights, then it will be set to
    default_weight, with a warning.

    Columns "lat" and "lon" are treated specially, in that they are
    not assigned a weight individually, but rather a single weight
    should be assigned to the "geo_dist" property.
    """
    weights = []
    weights_already_parsed = []
    for col in df.columns:
        if col in skip:
            continue
        weight_dict_key = col
        if col in ["lat", "lon"]:
            weight_dict_key = "geo_dist"
        if weight_dict_key in weights_already_parsed:
            continue
        weights_already_parsed.append(weight_dict_key)
        try:
            weight = pairwise_diff_weights[weight_dict_key]
            if weight is UndefinedConfigValue:
                raise KeyError
            weights.append(weight)
        except (KeyError):
            # If the user has not explicitely set the weight for this property
            if weight_dict_key == "geo_dist":
                weights.append(default_geodist)
            else:
                weights.append(default)
    return np.array(weights, dtype=np.float64)


def get_silhouette_samples(df, distance_matrix):
    # We will only consider true clusters for the calculation of
    # the silhouette coeff, i.e., points with label<0 will be excluded from
    # the calculation. This means that we need to use a slice of the distance
    # matrix in the calculation corresponding to the valid points.
    i_valid_obs = df.reset_index(drop=True).index[df["cluster_label"] >= 0]
    if len(i_valid_obs) == 0:
        logger.warn("No valid obs to calculate silhouette coeffs with")
        return -np.ones(len(df.index))

    reduced_labels = df["cluster_label"].iloc[i_valid_obs]
    if len(reduced_labels.unique()) == 1:
        logger.warn("Only one cluster to calculate silhouette coeffs with")
        return np.ones(len(df.index))

    reduced_dist_matrix = distance_matrix[i_valid_obs, :][:, i_valid_obs]
    # Using an intermediate np array is about 10x faster than
    # using df.at[iloc, 'silhouette_score'] = coeff
    all_silhouette_scores = np.empty(len(df.index))
    all_silhouette_scores[:] = np.nan

    reduced_silhouette_scores = metrics.silhouette_samples(
        X=reduced_dist_matrix, labels=reduced_labels, metric="precomputed"
    )
    for iloc, coeff in zip(i_valid_obs, reduced_silhouette_scores):
        all_silhouette_scores[iloc] = coeff

    return all_silhouette_scores


@njit(cache=True)
def get_rm_obs_label_offset(labels):
    """
    Integer value to be added to the cluster labels of outliers

    Constant integer value to be added to the cluster labels of
    the observations found to be outliers by our refinement schemes

    "labels" must be a numpy array for the numba jit compilation to work
    """
    rm_obs_label_offset = 10
    unique_labels = np.unique(labels)
    if unique_labels[0] < -1:
        max_abs_label = abs(unique_labels[0])
    else:
        max_abs_label = max(unique_labels[-1], 0)

    while max_abs_label % rm_obs_label_offset != max_abs_label:
        rm_obs_label_offset *= 10
    if unique_labels[0] < -1:
        rm_obs_label_offset //= 10

    return rm_obs_label_offset


# Routines related to the "iterative" outlier removal method
@njit(cache=True)
def _trim_np_array(array, perc, min_size=3):
    """Removes extreme valus from both sides of an array

    Takes an array and removes the "50*perc %" largest and
    "50*perc %" smallest elements, provided that the resulting
    trimmed array has a length no smaller tyan min_size
    """
    len_array = len(array)
    n_rm_each_side = int(abs(perc) * 0.5 * len_array)
    truncated_size = len_array - 2 * n_rm_each_side
    if (truncated_size != len_array) and (truncated_size >= min_size):
        array.sort()
        array = array[n_rm_each_side:-n_rm_each_side]
    return array


@njit(cache=True, parallel=True)
def _truncated_means_and_stds(df, perc, min_size=3):
    """
    Truncated means and stdevs for all columns in the dataframe df

    Takes a numpy version "df" of a pandas dataframe (obtained by
    calling the ".to_numpy" method on the original dataframe) and
    returns the truncated mean values and standard deviations for
    all columns. See the _trim_np_array routine for a description
    of the perc and min_size args.
    """
    ncols = df.shape[1]
    means = np.zeros(ncols)
    stds = np.zeros(ncols)
    for icol in prange(ncols):
        array = _trim_np_array(df[:, icol], perc, min_size)
        means[icol] = np.mean(array)
        stds[icol] = np.std(array)
    return means, stds


@njit(cache=True, parallel=True)
def _get_new_labels_for_deviating_obs_one_iter(
    df, max_n_stdev_around_mean, rm_obs_label_offset, truncate, weights
):
    """
    A single iteration of the _get_new_labels_for_deviating_obs function below
    """
    nrows, ncols = df.shape
    unique_labels = np.unique(df[:, -1])

    for label in unique_labels[unique_labels > -1]:
        indices_for_label = np.transpose(np.argwhere(df[:, -1] == label))[0]

        cols_taken_into_acc = []
        for icol in range(ncols - 1):
            if icol in [0, 1]:
                if weights[0] < 1e-3:
                    continue
            elif weights[icol - 1] < 1e-3:
                continue
            cols_taken_into_acc.append(icol)
        cols_taken_into_acc = np.array(cols_taken_into_acc)

        df_subset = df[indices_for_label, :][:, cols_taken_into_acc]
        means, stds = _truncated_means_and_stds(df_subset, truncate)
        tol = max_n_stdev_around_mean * stds[:]
        for irow in indices_for_label:
            for icol in cols_taken_into_acc:
                if np.abs(df[irow, icol] - means[icol]) > tol[icol]:
                    df[irow, -1] = -(df[irow, -1] + rm_obs_label_offset)
                    break

    return df


def _get_new_labels_for_deviating_obs(
    df,
    max_num_iter=100,
    max_n_stdev_around_mean=2.0,
    trunc_perc=0.0,
    weights=None,
    verbose=False,
):
    """
    Detects and assign new labels to obs where abs(obs[i]-obs_mean)>tolerance

    Helper function for the filter_outliers_iterative routine
    """
    nrows, ncols = df.shape
    if weights is None:
        weights = np.ones(ncols - 2)
    # Set any negative weight value to zero
    weights = np.where(weights < 0, 0.0, weights)

    unique_labels = np.unique(df[:, -1])
    rm_obs_label_offset = get_rm_obs_label_offset(unique_labels)

    n_removed_tot = 0
    for i in range(max_num_iter):
        if verbose:
            print("    > Refining scan, iteration ", i + 1, ": ", end=" ")
            start_time = time.time()
        n_removed_old = np.count_nonzero(df[:, -1] < -1)
        df = _get_new_labels_for_deviating_obs_one_iter(
            df,
            max_n_stdev_around_mean,
            rm_obs_label_offset,
            truncate=trunc_perc,
            weights=weights,
        )
        n_removed_new = np.count_nonzero(df[:, -1] < -1)
        n_removed_this_iter = n_removed_new - n_removed_old
        n_removed_tot = n_removed_tot + n_removed_this_iter
        if verbose:
            print("* rm ", n_removed_this_iter, end=" ")
            print(" stations, ", n_removed_tot, " so far. ", end=" ")
            print("Took ", time.time() - start_time, "s")
        if n_removed_this_iter == 0:
            break
    return df[:, -1]


def filter_outliers_iterative(
    df,
    skip,
    weights,
    trunc_perc=0.25,
    max_num_refine_iter=1000,
    max_n_stdev_around_mean=2,
    **kwargs
):
    df = df.rename(columns={"cluster_label": "original_cluster_label"})
    df["cluster_label"] = _get_new_labels_for_deviating_obs(
        df.drop(skip, axis=1).to_numpy(),
        max_num_iter=max_num_refine_iter,
        max_n_stdev_around_mean=max_n_stdev_around_mean,
        trunc_perc=trunc_perc,
        weights=weights,
        verbose=logger.getEffectiveLevel() == logging.DEBUG,
    ).astype(int)
    return df


# GLOSH outlier removal method
def filter_outliers_glosh(df, db, **kwargs):
    df["original_cluster_label"] = df["cluster_label"]
    df["GLOSH"] = db.outlier_scores_
    threshold = min(0.25, df[df["cluster_label"] > -1]["GLOSH"].quantile(0.75))
    outliers_index = (df["cluster_label"] > -1) & (df["GLOSH"] > threshold)
    rm_obs_label_offset = get_rm_obs_label_offset(
        df["cluster_label"].to_numpy()
    )
    df.at[outliers_index, "cluster_label"] = -(
        df["cluster_label"][outliers_index] + rm_obs_label_offset
    )
    return df


# Routines related to the LOF outlier removal method
def get_local_outlier_factors(df, distance_matrix, calc_per_cluster=False):
    # See <https://scikit-learn.org/stable/modules/generated/
    # sklearn.neighbors.LocalOutlierFactor.html#>
    unique_labels = df["cluster_label"].unique()
    all_lof_values = np.empty(len(df.index))
    all_lof_values[:] = np.nan
    # Is it better to do this in a per-cluster bases or
    # with the dataset as a whole? Maybe, with such a small
    # n_neighbors, the results won't change much.
    if calc_per_cluster:
        for label in unique_labels:
            if label < 0:
                continue
            indices_mask = df["cluster_label"] == label
            indices = df.index[indices_mask]
            reduced_dist_matrix = distance_matrix[indices, :][:, indices]
            clf = LocalOutlierFactor(
                n_neighbors=min(3, len(indices)), metric="precomputed"
            )
            clf.fit_predict(reduced_dist_matrix)
            all_lof_values[indices] = clf.negative_outlier_factor_
    else:
        indices_mask = df["cluster_label"] > -1
        indices = df.index[indices_mask]
        reduced_dist_matrix = distance_matrix[indices, :][:, indices]
        clf = LocalOutlierFactor(n_neighbors=3, metric="precomputed")
        clf.fit_predict(reduced_dist_matrix)
        all_lof_values[indices] = clf.negative_outlier_factor_
    return all_lof_values


def filter_outliers_lof(df, distance_matrix, **kwargs):
    df["original_cluster_label"] = df["cluster_label"]
    df["LOF"] = get_local_outlier_factors(df, distance_matrix)
    outliers_index = (df["cluster_label"] > -1) & (df["LOF"] < -1.5)
    rm_obs_label_offset = get_rm_obs_label_offset(
        df["cluster_label"].to_numpy()
    )
    df.at[outliers_index, "cluster_label"] = -(
        df["cluster_label"][outliers_index] + rm_obs_label_offset
    )
    return df


# "reclustering" outlier removal method
@suspendlogging
def filter_outliers_reclustering(df, distance_matrix, **kwargs):
    n_iter = 0
    n_removed = 0
    n_noise = np.count_nonzero(df["cluster_label"] < 0)
    while n_noise != 0:
        noise_mask = df["cluster_label"] < 0
        df_noise = df[noise_mask]

        i_valid_obs = np.nonzero((~noise_mask).values)[0]
        reduced_dist_matrix = distance_matrix[i_valid_obs, :][:, i_valid_obs]

        df = df.drop(df[noise_mask].index)
        df = df.drop(["cluster_label"], axis=1)
        df_rec = run_clustering_on_df(
            df,
            outlier_rm_method=None,
            sort_by_cluster_size=False,
            distance_matrix=reduced_dist_matrix,
            **kwargs,
        )
        n_noise = np.count_nonzero(df_rec["cluster_label"] < 0)
        df = pd.concat([df_noise, df_rec]).sort_index()
        n_iter += 1
        n_removed += n_noise
        logger.debug("        * Iter #%d: %d new noise pts", n_iter, n_noise)
    logger.debug("    > Done with reclustering. %d removed obs.", n_removed)
    return df


# General outlier removal routine, which calls the specific ones defined above
def filter_outliers(df, db, outlier_rm_method, distance_matrix, **kwargs):
    allowed_methods = dict(
        dbscan=["lof", "iterative", "reclustering"],
        hdbscan=["glosh", "lof", "iterative", "reclustering"],
    )
    clustering_method = "dbscan"
    if hasattr(db, "outlier_scores_"):
        clustering_method = "hdbscan"
    outlier_rm_method = outlier_rm_method.lower()
    if outlier_rm_method not in allowed_methods[clustering_method]:
        raise ValueError(
            'ERROR: Outlier removal method "{}" '.format(outlier_rm_method)
            + " not supported for {}.".format(clustering_method)
        )
    logger.debug('    > Running outlier rmv method "%s"', outlier_rm_method)
    tstart = time.time()
    if outlier_rm_method == "glosh":
        rtn = filter_outliers_glosh(df, db=db)
    elif outlier_rm_method == "lof":
        rtn = filter_outliers_lof(df, distance_matrix=distance_matrix)
    elif outlier_rm_method == "reclustering":
        rtn = filter_outliers_reclustering(df, distance_matrix, **kwargs)
    else:
        rtn = filter_outliers_iterative(df, **kwargs)
    logger.debug(
        "      * Done with outlier removal. Elapsed: %.1fs",
        time.time() - tstart,
    )
    return rtn


def sort_df_by_cluster_size(df):
    # Sort df so that clusters with more members are put at the top of the
    # dataframe. The exception if the "-1" label, whichm if present, will
    # always remain at the top. Handy if results are to be plotted.

    # The labels may have been reassigned if the df was passed through
    # an outlier removal routine. Let's keep track of the original ones.
    # This will help keeping obs removed from a cluster by the outlier
    # removed routine close to their origin cluster.
    original_cluster_label_col = "cluster_label"
    if "original_cluster_label" in df.columns:
        original_cluster_label_col = "original_cluster_label"

    # Temporarily add a column with cluster sizes for sorting
    unique_labels, member_counts = np.unique(
        df[original_cluster_label_col], return_counts=True
    )
    label2count_dict = {
        label: count for label, count in zip(unique_labels, member_counts)
    }
    df["parent_cluster_size"] = [
        label2count_dict[label] for label in df[original_cluster_label_col]
    ]
    # Sort dataframe according to frequency, but keep -1 at the top
    df = pd.concat(
        [
            df[df[original_cluster_label_col] == -1],
            df[df[original_cluster_label_col] != -1].sort_values(
                [
                    "parent_cluster_size",
                    original_cluster_label_col,
                    "cluster_label",
                ],
                ascending=[False, True, True],
            ),
        ]
    )

    # Reassign labels so that fewer members leads to larger labels.
    # Mind that the df unique method does not sort, so this method won't
    # mess up the sorting performed above.
    unique_labels = df[original_cluster_label_col].unique()
    labels_old2new = dict(
        (old, new)
        for new, old in enumerate(l for l in unique_labels if l >= 0)
    )
    labels_old2new[-1] = -1

    if original_cluster_label_col == "original_cluster_label":
        # This happens if some of the outlier removal routines are run.
        # If an observation is removed by such methods, it is helpful to
        # be able to know which cluster the obs was removed from.
        # Our convention throughout the code is to re-label the removed
        # obs according to:
        #
        #            new_label = -(old_label + rm_obs_label_offset),
        #
        # with the positive integer "rm_obs_label_offset" calculated
        # as in the get_rm_obs_label_offset function.
        #
        # Such a convention allows us to keep track of cluster origin for
        # removed obs without adding a new column to the dataframe. One
        # could think of just multiplying original labels by -1, but that
        # approach has two main problems:
        #    * Obs removed from label 0 would not be flagged
        #    * Obs removed from label 1 would be marked -1, but -1 is
        #      reserved for obs removed by the clustering itself
        rm_obs_label_offset = get_rm_obs_label_offset(
            df["cluster_label"].to_numpy()
        )

        # When building the labels_old2new dictionary after having reordered
        # the entries in the dataframe, we need to account for and keep using
        # this convention.
        for label in df["cluster_label"][df["cluster_label"] < -1].unique():
            cluster_it_was_rm_from = -np.rint(
                label + rm_obs_label_offset
            ).astype(int)
            labels_old2new[label] = -(
                labels_old2new[cluster_it_was_rm_from] + rm_obs_label_offset
            )

    new_labels = np.array([labels_old2new[old] for old in df["cluster_label"]])
    df["cluster_label"] = new_labels

    return df.drop("parent_cluster_size", axis=1).reset_index(drop=True)


def run_clustering_on_df(
    df,
    method="hdbscan",
    distance_matrix=None,
    skip=["id", "time_utc"],
    weights_dict={},
    eps=15,  # eps applies only to dbscan
    min_cluster_size=3,  # min_cluster_size applies only to hdbscan
    min_samples=3,
    n_jobs=-1,
    outlier_rm_method=None,
    max_num_refine_iter=50,
    max_n_stdev_around_mean=2.0,
    trunc_perc=0.25,
    sort_by_cluster_size=True,
    **kwargs
):

    method = method.lower()
    # Compute clustering using DBSCAN or HDBSCAN
    if method not in ["dbscan", "hdbscan", "rsl", "optics"]:
        raise NotImplementedError('Method "{}" not available.'.format(method))
    if len(df.index) == 0:
        raise ValueError("Dataframe has no rows")

    # Set weights to be used in the metrics for the various
    # generalised distances. The distances used in the metrics
    # will be used_dist(i) = weight(i)*real_dist(i)
    weights = get_weights_array(df, weights_dict)

    # We will not do any df = StandardScaler().fit_transform(df),
    # as we'll use a metric based on earth distances

    if distance_matrix is None:
        # My tests indicate that passing a pre-computed distance matrix to
        # dbscan can be up to 2.5x faster than passing a metrics function (if
        # they both are written in pure python) to fit df. If they are both
        # written in fortran and interfaced via f2py3, or then written in
        # python but jit-compiled with numba, then the relative speed up
        # can reach up to 120x.
        num_threads = -1
        if "num_threads" in kwargs:
            num_threads = kwargs["num_threads"]
        distance_matrix = calc_distance_matrix(
            # Drop columns that won't be used in the clustering
            df.drop(skip, axis=1),
            weights,
            num_threads,
        )

    # Running clustering with the computed distance matrix
    logger.debug('    > Running clustering method "{}"...'.format(method))
    tstart = time.time()
    if method == "dbscan":
        db = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric="precomputed",
            n_jobs=n_jobs,
        ).fit(distance_matrix)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
    elif method == "hdbscan":
        # For more info on the parameters, see
        # <https://hdbscan.readthedocs.io/en/latest/parameter_selection.html>
        db = HDBSCAN(
            min_samples=min_samples,
            min_cluster_size=min_cluster_size,
            metric="precomputed",
            core_dist_n_jobs=n_jobs,
            allow_single_cluster=True,
            # Default cluster_selection_method: 'eom'. Sometimes it leads to
            # clusters that are too big. Using 'leaf' seems better.
            cluster_selection_method="leaf",
            # cluster_selection_epsilon=7.5,
        ).fit(distance_matrix)
        # core_samples info is not available with hdbscan
        core_samples_mask = None
    elif method == "rsl":
        db = RobustSingleLinkage(
            # cut: The reachability distance value to cut the cluster
            #      heirarchy at to derive a flat cluster labelling.
            cut=eps,  # default=0.4
            # Reachability distances will be computed with regard to the
            # k nearest neighbors.
            k=min_samples,  # default=5
            # Ignore any clusters in the flat clustering with size less
            # than gamma, and declare points in such clusters as noise points.
            gamma=min_cluster_size,  # default=5
            metric="precomputed",
        ).fit(distance_matrix)
        # core_samples info is not available with rsl
        core_samples_mask = None
    elif method == "optics":
        db = OPTICS(
            min_samples=min_samples,
            min_cluster_size=min_cluster_size,
            n_jobs=n_jobs,
            metric="precomputed",
        ).fit(distance_matrix)
        # core_samples info is not available with optics
        core_samples_mask = None
    logger.debug(
        "      * Done with {0}. Elapsed: {1:.1f}s".format(
            method, time.time() - tstart
        )
    )
    # Update df with cluster label info. It is important that this is done
    # right before calling _get_new_labels_for_deviating_obs, as the
    # _get_new_labels_for_deviating_obs functions expects 'cluster_label'
    # to be the last column in the dataframe
    df["cluster_label"] = db.labels_

    # Refine clustering if requested
    # It is important to have 'cluster_label' as the last column
    # when running the iterative refine routine
    if outlier_rm_method:
        df = filter_outliers(
            df,
            db=db,
            outlier_rm_method=outlier_rm_method,
            # Args that apply only to LOF
            distance_matrix=distance_matrix,
            # Args that only apply for the iterative method
            skip=skip,
            max_num_refine_iter=max_num_refine_iter,
            max_n_stdev_around_mean=max_n_stdev_around_mean,
            trunc_perc=trunc_perc,
            weights=weights,
            method=method,
            weights_dict=weights_dict,
            eps=eps,
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            n_jobs=n_jobs,
        )

    # core_samples_mask is only returned by dbscan, not by hdbscan
    if core_samples_mask is not None:
        df["is_core_point"] = core_samples_mask

    # Calculate silhouette scores and update df with this.
    # We'll be reordering the dataframe later, and calculating the score
    # before doing that avoids the need to also reorder the dist matrix.
    df["silhouette_score"] = get_silhouette_samples(df, distance_matrix)

    if sort_by_cluster_size:
        df = sort_df_by_cluster_size(df)

    # Remove aux columns that are no longe rneeded
    try:
        df = df.drop("original_cluster_label", axis=1)
    except (KeyError):
        pass

    return df


def cluster_netatmo_obs(
    config,
    dtg=None,
    sort_by_cluster_size=False,
    return_list_of_removed_stations=False,
    **kwargs
):
    if dtg is None:
        dtg = config.dtgs[0]
    logger.debug("Reading data for DTG=%s...", dtg)
    start_read_data = time.time()
    if return_list_of_removed_stations:
        df, rmvd_stations = read_netatmo_data_for_dtg(
            dtg,
            rootdir=config.data_rootdir,
            return_list_of_removed_stations=True,
        )
    else:
        df = read_netatmo_data_for_dtg(dtg, rootdir=config.data_rootdir)
    end_read_data = time.time()
    logger.debug(
        "Done reading data for DTG={}. Elapsed: {:.1f}s".format(
            dtg, end_read_data - start_read_data
        )
    )

    time_start_clustering = time.time()
    logger.debug("Performing clustering...")
    df = run_clustering_on_df(
        df=df,
        method=config.clustering_method,
        weights_dict=config.get("obs_weights", {}),
        eps=config.get("eps", 10),
        min_cluster_size=config.get("min_cluster_size", 5),
        min_samples=config.get("min_samples", 5),
        outlier_rm_method=config.outlier_removal.method,
        max_num_refine_iter=config.get("outlier_removal.max_n_iter", 1000),
        max_n_stdev_around_mean=config.get("outlier_removal.max_n_stdev", 2),
        # We only need this sorting if we're plotting
        sort_by_cluster_size=sort_by_cluster_size,
        **kwargs,
    )
    time_end_clustering = time.time()
    logger.debug(
        "Done with clustering. Elapsed: {}s".format(
            np.round(time_end_clustering - time_start_clustering, 2)
        )
    )

    if return_list_of_removed_stations:
        return df, rmvd_stations
    else:
        return df


def report_clustering_results(df):
    n_obs = len(df.index)
    noise_data_df = df[df["cluster_label"] < 0]
    n_noise_clusters = len(noise_data_df["cluster_label"].unique())
    noise_count = len(noise_data_df)
    n_clusters = len(df["cluster_label"].unique()) - n_noise_clusters
    n_accepted = n_obs - noise_count
    silhouette_score = df["silhouette_score"].mean(skipna=True)

    logger.info("Total number of parsed observations: %d", n_obs)
    logger.info("Estimated number of clusters: %d", n_clusters)
    logger.info("Estimated number of accepted obs: %d", n_accepted)
    logger.info(
        "Estimated number of noise obs: %d (%.1f%% rejection rate)",
        noise_count,
        100.0 * noise_count / n_obs,
    )
    logger.info("Mean silhouette score: {:.3f}".format(silhouette_score))
