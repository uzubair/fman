""" Utilities """

import logging
import os
import fnmatch

log = logging.getLogger("i.utils")


def execution_time(duration):
    mins, secs = divmod(duration, 60)
    hours, mins = divmod(mins, 60)
    return hours, mins, secs


def is_directory(path):
    return os.path.isdir(path)


def is_file(path):
    return os.path.isfile(path)


def get_size(path):
    return os.path.getsize(path)


def ls(path, filter):
    fresults = {}
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            try:
                fpath = os.path.join(root, filename)
                rpath = os.path.realpath(fpath)
                size = get_size(rpath)
                if filter:
                    if fnmatch.fnmatch(filename, '*%s*' % filter):
                        fresults[rpath] = size
                else:
                    fresults[rpath] = size
            except OSError as e:
                # Permissions issues for symlinked files
                # pass on
                continue
    return fresults
