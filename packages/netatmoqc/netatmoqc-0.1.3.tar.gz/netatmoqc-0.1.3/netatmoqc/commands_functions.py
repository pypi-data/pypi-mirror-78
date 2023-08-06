import logging
import argparse
import subprocess
import platform
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
import time
import os
import sys
import psutil
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from functools import partial
from netatmoqc.config_parser import read_config
from netatmoqc.dtgs import Dtg
from netatmoqc.logs import get_logger
from netatmoqc.mpi import mpi_parallel
from netatmoqc.plots import (
    make_clustering_fig,
    show_cmd_get_fig_from_dataframes,
)
from netatmoqc.load_data import (
    rm_moving_stations,
    DataNotFoundError,
)
from netatmoqc.clustering import cluster_netatmo_obs, report_clustering_results

logger = logging.getLogger(__name__)

CYAN = "\u001b[36m"
RESET_COLOUR = "\u001b[0m"


def cluster_obs_single_dtg(args):
    """ Implements the "cluster" command """

    try:
        dtg = Dtg(args.dtg)
    except (TypeError):
        dtg = None
    config = read_config(args.config_file)
    if dtg is None:
        dtg = config.dtgs[0]
    logger.info(
        "Running %s on obs for " + CYAN + "DTG=%s" + RESET_COLOUR + "...",
        config.clustering_method,
        dtg,
    )
    df = cluster_netatmo_obs(
        config, dtg=args.dtg, sort_by_cluster_size=(args.show or args.savefig)
    )
    report_clustering_results(df)
    if args.show or args.savefig:
        logger.info("Preparing figure...")
        fig = make_clustering_fig(df)
        if args.savefig:
            fig.write_html("cluster_obs_single_dtg.html")
        if args.show:
            fig.show()
    logger.info("Done.")


def _select_stations_single_dtg(dtg, config, args):
    """ This is what "select_stations" does for each DTG """

    logger = get_logger(__name__, args.loglevel)
    logger.info(CYAN + "DTG=%s" + RESET_COLOUR + ": Started", dtg)

    # Some control of oversubscription if using mpi.
    # This is not needed when using single-host joblib with "loky"
    cpu_share = -1
    if args.mpi:
        proc_parent = psutil.Process(os.getppid())
        proc_family_size = len(proc_parent.children())
        cpu_share = multiprocessing.cpu_count() // proc_family_size

    tstart = time.time()
    try:
        df, rmvd_stations = cluster_netatmo_obs(
            config,
            dtg,
            return_list_of_removed_stations=True,
            num_threads=cpu_share,
        )
    except DataNotFoundError as e:
        logger.warning(e)
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    selected_cols = ["id", "lat", "lon", "alt"]
    rejected_stat_mask = df["cluster_label"] < 0
    rejected_stations = df[selected_cols][rejected_stat_mask]
    accepted_stations = df[selected_cols][~rejected_stat_mask]
    moving_stations = rmvd_stations[selected_cols]

    logger.info("DTG=%s: Done. Elapsed: %.1fs", dtg, time.time() - tstart)
    return accepted_stations, rejected_stations, moving_stations


def select_stations(args):
    """ Implements the "select" command

    This function calls "_select_stations_single_dtg" for each DTG
    (in parallel if requested/possible), and then processes, gathers
    and saves the results.
    """

    tstart_selection = time.time()
    config = read_config(args.config_file)

    # Process DTGs in parallel if possible/requested
    if args.mpi:
        logger.info("Parallelising tasks over DTGs using MPI")
        func = partial(_select_stations_single_dtg, config=config, args=args)
        results = mpi_parallel(func, config.dtgs)
    else:
        logger.info("Parallelising tasks over DTGs within a single host")
        # Using the "loky" backend helps avoiding oversubscription
        # of cpus in child processes
        n_procs = int(os.getenv("NETATMOQC_MAX_PYTHON_PROCS", 1))
        with parallel_backend("loky"):
            results = Parallel(n_jobs=n_procs)(
                delayed(_select_stations_single_dtg)(dtg, config, args)
                for dtg in config.dtgs
            )
    logger.info(
        "End of survey over %d DTGs. Combining results..." + "\n",
        len(config.dtgs),
    )
    # Gather results: Only accepted and rejected stations for now. Moving
    # stations will be handled after post-processing accepted and rejected
    accepted_stations = pd.concat((r[0] for r in results), ignore_index=True)
    rejected_stations = pd.concat((r[1] for r in results), ignore_index=True)

    accepted_stations, moving_accepted_stations = rm_moving_stations(
        accepted_stations
    )
    if len(moving_accepted_stations.index) > 0:
        logger.warning(
            'Removed %d "moving" stations from the list of accepted stations',
            len(moving_accepted_stations["id"].unique()),
        )

    rejected_stations, moving_rejected_stations = rm_moving_stations(
        rejected_stations
    )
    if len(moving_rejected_stations.index) > 0:
        logger.warning(
            'Removed %d "moving" stations from the list of removed stations',
            len(moving_rejected_stations["id"].unique()),
        )

    # Let's recover some stations for the list of rejected if they
    # also appear among the accepted_stations. Do this based on a
    # tolerance criteria.
    logger.info(
        "Applying station_rejection_tol=%.2f to rescue "
        + 'stations from the "rejected" list',
        config.commands.select.station_rejection_tol,
    )
    accept_counts_per_id = accepted_stations["id"].value_counts()
    reject_counts_per_id = rejected_stations["id"].value_counts()
    rescued_rejected_stats = []
    for stat_id in reject_counts_per_id.index:
        reject_count = reject_counts_per_id[stat_id]
        try:
            accept_count = accept_counts_per_id[stat_id]
        except (KeyError):
            accept_count = 0
        rejection_rate = 1.0 * reject_count / (reject_count + accept_count)
        if rejection_rate < config.commands.select.station_rejection_tol:
            rescued_rejected_stats.append(stat_id)
    # Using a rescued_rejected_stats list to modify the dataframes
    # accepted_stations/rejected_stations is much faster than modifying
    # the dataframes inside the loop above
    rescued_rows = rejected_stations.loc[
        rejected_stations["id"].isin(rescued_rejected_stats), :
    ]
    accepted_stations = accepted_stations.append(
        rescued_rows, ignore_index=True
    )
    rejected_stations = rejected_stations.drop(rescued_rows.index)
    if len(rescued_rejected_stats) > 0:
        logger.info(
            "    > Rescuing %d stations rejected in less than %.1f%% of "
            + "occurences",
            len(rescued_rejected_stats),
            100 * config.commands.select.station_rejection_tol,
        )
    else:
        logger.info('    > No stations recovered from "rejected"')

    # We don't need duplicate entries
    accepted_stations = accepted_stations.drop_duplicates(subset=["id"])
    rejected_stations = rejected_stations.drop_duplicates(subset=["id"])

    # Now we can handle moving stations
    moving_stations = pd.concat(
        [r[2] for r in results]
        + [moving_accepted_stations, moving_rejected_stations,],
        ignore_index=True,
    )
    unique_moving_stations = moving_stations["id"].unique()

    rejected_stations = rejected_stations[
        ~rejected_stations["id"].isin(unique_moving_stations)
    ]
    accepted_stations = accepted_stations[
        ~(
            accepted_stations["id"].isin(unique_moving_stations)
            | accepted_stations["id"].isin(rejected_stations["id"])
        )
    ]
    if len(unique_moving_stations) > 0:
        logger.warning(
            "\n A total of %d unique stations were removed from both\n"
            + " accepted and rejected lists because they changed\n"
            + " at least one of (lat, lon, alt) throughout the survey\n"
            + " These will be saved separately in the moving_stations.csv file",
            len(unique_moving_stations),
        )

    total_nstations = sum(
        map(
            len,
            [
                accepted_stations.index,
                rejected_stations.index,
                unique_moving_stations,
            ],
        )
    )
    n_selected = len(accepted_stations.index)
    ratio = 100.0 * n_selected / total_nstations

    elapsed = time.time() - tstart_selection
    logger.info(
        "Station selection over %d DTGs performed in %.1fs (~%.1fs per DTG)"
        + "\n",
        len(config.dtgs),
        elapsed,
        elapsed / len(config.dtgs),
    )

    logger.info(
        "%d stations (%.2f%% out of %d) "
        + "were consistently accepted throughout the survey",
        n_selected,
        ratio,
        total_nstations,
    )
    logger.info(
        "That's %d rejections (%.2f%% rejection rate)",
        total_nstations - n_selected,
        100.0 - ratio,
    )

    # Saving results
    fpath = Path().resolve() / "accepted_stations.csv"
    logger.info("Saving accepted stations data to %s", fpath)
    accepted_stations.to_csv(fpath, index=None, mode="w")

    fpath = Path().resolve() / "rejected_stations.csv"
    logger.info("Saving rejected station data to %s", fpath)
    rejected_stations.to_csv(fpath, index=None, mode="w")

    fpath = Path().resolve() / "moving_stations.csv"
    logger.info("Saving moving stations data to %s", fpath)
    moving_stations.to_csv(fpath, index=None, mode="w")

    if args.show or args.savefig:
        accepted_stations["cluster_label"] = np.zeros(
            len(accepted_stations.index)
        )
        rejected_stations["cluster_label"] = -np.ones(
            len(rejected_stations.index)
        )

        if len(moving_stations.index) > 0:
            statid2label_dict = dict(
                (statid, -(i + 12))
                for i, statid in enumerate(unique_moving_stations)
            )

            @np.vectorize
            def statid2label(sid):
                return statid2label_dict[sid]

            moving_stations["cluster_label"] = statid2label(
                moving_stations["id"]
            )

        df = pd.concat(
            [rejected_stations, moving_stations, accepted_stations],
            ignore_index=True,
        )
        logger.info("Preparing figure...")
        fig = make_clustering_fig(df)
        if args.savefig:
            fig.write_html("select_stations.html")
        if args.show:
            fig.show()


# Code related to the "show" command
def _open_file_with_default_app(fpath):
    if platform.system() == "Windows":
        os.startfile(fpath)
    elif platform.system() == "Darwin":
        subprocess.call(("open", fpath))
    else:
        subprocess.call(("xdg-open", fpath))


def show(args):
    """ Implements the 'show' command """

    logger = get_logger(__name__, args.loglevel)

    dataframes = {}
    for fpath in args.file_list:
        if fpath.suffix == ".csv":
            logger.info("Reading data from file %s", fpath)
            dataframes[fpath.name] = pd.read_csv(fpath)
        elif fpath.suffix in [".htm", ".html"]:
            logger.info("Openning file '%s'", fpath)
            _open_file_with_default_app(fpath)
        else:
            logger.warning(
                "Only html and csv files supported. Skipping file '%s'", fpath
            )

    if len(dataframes) > 0:
        fig = show_cmd_get_fig_from_dataframes(args, dataframes)
        fig.show()
