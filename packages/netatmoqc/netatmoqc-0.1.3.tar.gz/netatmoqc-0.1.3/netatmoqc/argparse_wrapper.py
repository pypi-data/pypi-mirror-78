import argparse
from datetime import datetime
import subprocess
import os
from pathlib import Path
from netatmoqc.commands_functions import (
    cluster_obs_single_dtg,
    select_stations,
    show,
)


def get_parsed_args(program_name):
    # Define main parser and general options
    parser = argparse.ArgumentParser(
        prog=program_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    try:
        fpath = Path(os.getenv("NETATMOQC_CONFIG_PATH", "config.toml"))
        default_conf_path = fpath.resolve(strict=True)
    except (FileNotFoundError):
        default_conf_path = (
            Path(os.getenv("HOME")) / ".netatmoqc" / "config.toml"
        )
    parser.add_argument(
        "-config_file",
        metavar="CONFIG_FILE_PATH",
        default=default_conf_path,
        type=Path,
        help=(
            "Path to the config file. The default is whichever of the "
            + "following is first encountered: "
            + "(i) The value of the 'NETATMOQC_CONFIG_PATH' envvar or "
            + "(ii) './config.toml'. If both (i) and (ii) are missing, "
            + "then the default will become "
            + "'"
            + str(Path("$HOME/.netatmoqc/config.toml"))
            + "'"
        ),
    )
    parser.add_argument(
        "-loglevel",
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "notset"],
        help="What type of info should be printed to the log",
    )
    parser.add_argument(
        "--mpi",
        action="store_true",
        help=(
            "Enable MPI parallelisation in some parts of the code. "
            + "Requires that the code be installed with support to MPI."
        ),
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Open a browser window to show results on a map",
    )
    parser.add_argument(
        "--savefig",
        action="store_true",
        help="Saves an html file showing results on a map",
    )

    # Configure the main parser to handle the commands
    # From python v3.7, add_subparsers accepts a 'required' arg. We
    # could use required=True in the definition below, but, since we
    # want to be able to use python >= 3.6.10, we won't. The requirement
    # of having a command passed will be enforced in the main.py file.
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        description=(
            "Valid commands for {0} (note that commands also accept their "
            + "own arguments, in particular [-h]):"
        ).format(program_name),
        help="command description",
    )

    # Configure parser for the "cluster" command
    parser_cluster = subparsers.add_parser(
        "cluster", help="Run cluster on NetAtmo obs for a single DTG"
    )
    parser_cluster.add_argument(
        "-dtg",
        type=lambda s: datetime.strptime(s, "%Y%m%d%H"),
        default=None,
        help="""
        If not passed, then the first DTG in the config file will be used.
        """,
    )
    parser_cluster.set_defaults(func=cluster_obs_single_dtg)

    # Configure parser for the "select" command
    parser_select = subparsers.add_parser(
        "select",
        help="Select NetAtmo stations via clustering over a range of DTGs",
    )
    parser_select.set_defaults(func=select_stations)

    # Configure parser for the "apps" command
    parser_apps = subparsers.add_parser(
        "apps", help="Start a server for the provided Dash apps"
    )
    parser_apps.set_defaults(
        func=lambda args: subprocess.run(
            [
                "sh",
                Path(__file__).parent.resolve() / "bin" / "start_apps",
                args.config_file.resolve(),
            ]
        )
    )

    # Configure parser for the "show" command
    parser_show = subparsers.add_parser(
        "show", help="Reads netatmoqc results fron file and displays them"
    )
    parser_show.add_argument(
        "file_list",
        nargs="*",
        type=Path,
        default=list(Path(".").glob("*.csv")),
        help="List of files from where the results should be read",
    )
    parser_show.set_defaults(func=show)

    args = parser.parse_args()

    return args
