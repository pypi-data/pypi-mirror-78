#!/usr/bin/env python3
from netatmoqc.logs import get_logger
from pathlib import Path
import sys
from netatmoqc.argparse_wrapper import get_parsed_args


def main():
    prog_name = Path(sys.argv[0]).name
    args = get_parsed_args(prog_name)
    logger = get_logger(prog_name, args.loglevel)
    if args.command is None:
        # Enforce this here instead of on the command's parser.add_subparsers
        # definition because add_subparsers only introduced the "required" arg
        # from python v3.7, and we want the code to work with python>=3.6.10.
        msg = "Cannot run {0} without a command! Please run "
        msg += "'{0} -h' for help."
        msg = msg.format(prog_name)
        logger.error(msg)
        sys.exit(1)
    args.func(args)
