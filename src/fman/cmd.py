""" Console entrypoint """

import logging
import os
import timeit
from argparse import ArgumentParser
from fman.utils import execution_time
from fman.fmanager import find, duplicate
from fman.task import TaskManager

log = logging.getLogger("i.cmd")


def main():
    # Main console entrypoint.
    start_time = timeit.default_timer()

    if "DEBUG" in os.environ:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser(description="A simple command-line utility to manage files")
    subparser = parser.add_subparsers(help="Supported operations")

    _find = subparser.add_parser("find", help="Find files")
    _find.set_defaults(func=find, msg="Starting to find the files")
    _find.add_argument(
        "-p", "--path", help="The path of the directory", nargs="+", required=True
    )
    _find.add_argument("-f", "--filter", help="Search files meeting specific criteria e.g. *.mp3", type=str)

    _duplicate = subparser.add_parser("duplicate", help="Find duplicates")
    _duplicate.set_defaults(func=duplicate, msg="Starting to find duplicate files")
    _duplicate.add_argument("-p", "--path", help="The path of the directory", nargs="+", required=True)

    args = parser.parse_args()

    log.info(args.msg)

    task_manager = TaskManager(args)
    task_manager.execute()

    duration = timeit.default_timer() - start_time
    hours, mins, secs = execution_time(duration)
    log.info("Done in %d:%d:%.2f" % (hours, mins, secs))
