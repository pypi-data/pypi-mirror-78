#!/usr/bin/env python3
import numpy as np
import time
import numba
from numba import njit, prange
import logging
import atexit

logger = logging.getLogger(__name__)


@njit(cache=True)
def _matrix_index_to_data_index(order, i, j):
    """Convert (i, j) index into single data index for a sparse dist matrix

    Given a square matrix M of order "order" which also satisfies
                M(i, j) = M(j, i) and M(i, i) = 0
    and a linear array, say "M_data" that stores only the independent elements
    of M, return the index i_data such that
                M(i, j) = M_data(i_data)

    This routine assumes
                        0 <= i,j < order
    To make using numba.jit easier, no checks
    are performed on indices, but, if there's a possibility that users will
    have access to this functionality, then one should ideally expose a
    wrapper that performs such checks before calling this function.

    This function is used in the SparseSymmZeroDiagMatrix class, where
    consistency between the arguments is enforced.
    """

    # Start by enforcing M(i, j) = M(j, i)
    if i > j:
        i, j = j, i

    # n_indep_els_before_row: Total number of independent elements
    # located in the rows prior to row=i for the matrix M
    n_indep_els_before_row = i * order - (i * (i + 1)) // 2

    return n_indep_els_before_row + (j - i - 1)


@njit(cache=True)
def _data_index_to_matrix_index(n, i_data):
    """Convert linear data index into matrix indices

    Given a square matrix M of order "n" which also satisfies
                M(i, j) = M(j, i) and M(i, i) = 0
    and a linear array, say "M_data" that stores only the independent elements
    of M, return the matrix indices (i, j) such that
                M(i, j) = M_data(i_data)
    This is the inverse of what is done in _matrix_index_to_data_index.

    This routine assumes
                        0 <= i_data < n(n-1)/2
    To make using numba.jit easier, no checks are performed on i_data,
    but, if there's a possibility that users will have access to this
    functionality, then one should ideally expose a wrapper that performs
    such checks before calling this function.

    This function is used in the SparseSymmZeroDiagMatrix class, where
    consistency between the arguments is enforced.
    """
    i = (
        int(0.5 * ((2 * n + 1) - np.sqrt((2 * n + 1) ** 2 - 8 * (n + i_data))))
        - 1
    )
    j = (1 + i_data + i) - (i * (2 * n - i - 1)) // 2
    return i, j


@njit(cache=True, parallel=True)
def _to_dense(data, n, dtype=None, copy=None, order=None):
    """Dense form of sparse matrix M with data 'data', M(i,j)=M(j,i), M(i,i)=0

    Takes an array 'data' and an integer 'n' and constructs a full (dense)
    representation of a square matrix M of order 'n' such that
                       M(i,j)=M(j,i), M(i,i)=0
    and whose independent elements are stored sequentially in 'data'.

    Assumes that len(data) = n*(n - 1)/2.
    No checks, however, are made on len(data). If you want to provide this
    functionality in an external API, please expose a wrapper to this function
    where this is asserted.

    This function is used in the SparseSymmZeroDiagMatrix class, where
    consistency between the arguments is enforced.

    The args dtype, copy and order are ignored, but this interface was
    necessary in order to be able to use the optics clustering method.
    """
    dense = np.zeros(shape=(n, n))
    for idata in prange(len(data)):
        i, j = _data_index_to_matrix_index(n, idata)
        data_value = data[idata]
        dense[i, j] = data_value
        dense[j, i] = data_value
    return dense


class SparseSymmZeroDiagMatrix:
    """Sparse, square, symmetric matrix with zeros along the diagonal

    The order N of the (N, N) matrix is calculated from the passed data array.
    The diagonal elements are not stored (assumed to be all zero), and only
    half of the remaining elements are stored, as M(i, j) = M(j, i).
    """

    def __init__(self, data):
        # N: Order N of the NxN square matrix M(i, j)
        # n_indep: Number of independent elements
        #     Since M is symmetric and diagnonal elements are always zero,
        #     n_indep = (N**2 - N)/2
        n_indep = len(data)
        N = 0.5 * (1.0 + np.sqrt(1.0 + 8.0 * n_indep))
        nearest_int_N = int(np.rint(N))
        if abs(N - nearest_int_N) > 1e-8:
            nearest_n_indep = int(0.5 * nearest_int_N * (nearest_int_N - 1))
            msg = "len(data)={0} incompatible with an NxN distance matrix: "
            msg += "{1} elements needed for a {2}x{2} matrix (closest option)"
            msg = msg.format(n_indep, nearest_n_indep, nearest_int_N)
            raise ValueError(msg)
        self._order = int(np.rint(N))
        self._data = np.array(data)

    @property
    def order(self):
        return self._order

    @property
    def shape(self):
        return (self.order, self.order)

    @property
    def data(self):
        return self._data

    def matrix_index_to_data_index(self, i, j):
        """Returns an integer I such that self.data[I] == self[i, j]"""
        if i >= self.order:
            raise IndexError(
                "index {} is out of bounds for axis 1 with size {}".format(
                    i, self.order
                )
            )
        if j >= self.order:
            raise IndexError(
                "index {} is out of bounds for axis 1 with size {}".format(
                    j, self.order
                )
            )
        return _matrix_index_to_data_index(self.order, i, j)

    def data_index_to_matrix_index(self, data_i):
        """Returns (i, j) such that self.data[data_i] == self[i, j]"""
        if data_i >= len(self.data):
            raise IndexError(
                "index {} is out of bounds for axis 1 with size {}".format(
                    data_i, self.data
                )
            )
        return _data_index_to_matrix_index(self.order, data_i)

    def __array__(self, dtype=None, copy=False, order=None):
        # See <https://numpy.org/devdocs/user/basics.dispatch.html>
        return _to_dense(self.data, self.order, dtype, copy, order)

    def __getitem__(self, ij_tuple):
        if any(isinstance(index, slice) for index in ij_tuple):
            # TODO: Implement a proper getitem for slices.
            #       This is fast but not memory-efficient,
            #       as it creates a full version of the array
            return self.copy()[ij_tuple]
        else:
            if ij_tuple[0] == ij_tuple[1]:
                return 0.0
            else:
                return self.data[self.matrix_index_to_data_index(*ij_tuple)]

    def copy(self):
        # TODO: Make a proper copy implementation. This is a quick fix
        # because I need this for hdbscan.
        # self._cached_array_copy will hold a copy of the dense representation
        # of self if the self.copy method is ever called. This, of course,
        # increases memory usage, but HDBSCAN seems to call the self.copy
        # method 3 times, and having a cache leads to non-negligible savings
        # in runtime for large datasets.
        try:
            return self._cached_array_copy
        except (AttributeError):
            self._cached_array_copy = np.asarray(self)
            return self._cached_array_copy


# Routines related to the calculation of the distance matrix
@njit(cache=True)
def haversine_distance(point1, point2):
    lat1 = np.deg2rad(point1[0])
    lat2 = np.deg2rad(point2[0])
    dlat = lat2 - lat1
    dlon = np.deg2rad(point2[1] - point1[1])
    a = (
        np.sin(dlat * 0.5) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon * 0.5) ** 2
    )
    # earth_mean_diameter = 12742.0176 Km
    rtn = 12742.0176 * np.arcsin(np.sqrt(a))
    return rtn


@njit(cache=True)
def get_obs_norm_factors(obs_values):
    stdev = np.std(obs_values)
    obs_mean = np.mean(obs_values)
    if (
        (abs(obs_mean) > 1e-5 and abs(stdev / obs_mean) < 1e-5)
        or abs(obs_mean) <= 1e-5
        and stdev < 1e-7
    ):
        rtn = 0.0
    else:
        rtn = 1.0 / stdev
    return rtn


@njit("f4[:](f8[:, :], f8[:])", parallel=True, cache=True)
def calc_distance_matrix_numba(df, weights):
    nrows, ncols = df.shape

    # Get normalisation factors so that observations in different
    # scales have comparable diff values
    # Remember: The first entry in weights refers to geo_dist and
    #           the first two columns of df are (lat, lon)
    obs_norm_factors = np.ones(ncols - 1, dtype=np.float32)
    for i in range(1, len(obs_norm_factors)):
        obs_norm_factors[i] = get_obs_norm_factors(df[:, i + 1])

    # weights can be used by the users to give extra or
    # lower weight to a given observation type. The weights
    # are applied to the normalised values of the obd diffs
    #
    # We are not normalising geodists. Therefore, the normalised obs
    # dists should have the same units as the geodists (km).
    # Let's assign 10 km/normalized_obs_unit_diff by default
    # This unit conversion is highly arbitrary...

    weights_internal = weights
    # Set any negative weight value to zero
    weights_internal = np.where(weights_internal < 0, 0.0, weights_internal)
    weights_internal *= obs_norm_factors

    n_dists = (nrows * (nrows - 1)) // 2
    rtn = np.zeros(n_dists, dtype=np.float32)
    # For better parallel performance, loop over single idist instead of doing
    # a nested "for i in prange(nrows): for j in range(i+1, nrows):".
    # If one wishes to reverse this, then use func _matrix_index_to_data_index
    # or note that idist = i*nrows - i*(i+1)//2 + (j - i - 1)
    # NB.: Initialising i and j as integers, otherwise numba v0.50.1 fails
    # silently and gives wrong results in python 3.8 with "parallel=True".
    # Strangely, the results are correct without initialisation when using
    # python 3.6 or when setting parallel=False.
    i, j = np.zeros(2, dtype=np.int64)
    for idist in prange(n_dists):
        i, j = _data_index_to_matrix_index(nrows, idist)
        rtn[idist] = weights_internal[0] * haversine_distance(
            df[i], df[j]
        ) + np.sum(
            np.sqrt((weights_internal[1:] * (df[j, 2:] - df[i, 2:])) ** 2)
        )

    return rtn


def calc_distance_matrix(df, weights, num_threads=-1):
    logger.debug("    > Calculating distance matrix...")
    tstart = time.time()

    if num_threads > 0:
        original_nthreads = numba.get_num_threads()
        numba.set_num_threads(num_threads)
        atexit.register(numba.set_num_threads, original_nthreads)

    rtn = SparseSymmZeroDiagMatrix(
        data=calc_distance_matrix_numba(df.to_numpy(), weights=weights)
    )

    logger.debug(
        "      * Done calculating distance matrix. "
        + "Elapsed: {:.1f}s".format(time.time() - tstart)
    )
    return rtn
