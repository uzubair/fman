"""  Console entrypoint """

import logging
import os
import timeit
from argparse import ArgumentParser
from fman.utils import execution_time, is_directory
from fman.fmanager import find, duplicate
from fman.task import ThreadPoolManager


log = logging.getLogger("i.cmd")


def run(options):
    # Performs the selected op
    thread_pool_manager = ThreadPoolManager(num_threads=2)
    num_paths = len(options.path)
    fresults = {}
    for i, path in enumerate(options.path, 1):
        log.info("Processing {} of {}. Path = '{}'".format(i, num_paths, path))
        if not is_directory(path):
            log.info(f"{path} is not a valid directory!")
            continue
        thread_pool_manager.add_task(options.func, path, options.filter, fresults)
    thread_pool_manager.wait_completion()
    log.info("Found {} files".format(len(fresults)))
    for file, size in fresults.items():
        print("{}={}".format(file, size))


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

    run(args)

    duration = timeit.default_timer() - start_time
    hours, mins, secs = execution_time(duration)
    log.info("Done in %d:%d:%.2f" % (hours, mins, secs))
