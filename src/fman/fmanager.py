import logging
import hashlib
from collections import defaultdict
from fman.utils import is_directory, is_file, ls


log = logging.getLogger("i.fmanager")


def chunk_reader(file, chunk_size=1024):
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield chunk

def get_hash(fpath, first_chunk=True):
    hash_obj = hashlib.sha1()
    with open(fpath, 'rb') as _file:
        if first_chunk:
            hash_obj.update(_file.read(1024))
        else:
            for chunk in chunk_reader(_file):
                hash_obj.update(chunk)
    hashed = hash_obj.digest()
    return hashed

def find(path, options):
    if not is_directory(path):
        log.info(f"{path} is not a valid directory!")
        return None
    return path, ls(path, options.filter)

def duplicate(path, options):
    _, files = find(path, options)
    hashes = defaultdict(list)
    for fpath, size in files.items():
        hashes[size].append(fpath)

    # Get 1st 1024 bytes hash for files with same file size
    for size, fpaths in hashes.items():
        # Only one file found, let's not waste CPU cycle on it
        if len(fpaths) < 2:
            continue
        for fpath in fpaths:
            try:
                fhash = get_hash(fpath, first_chunk=True)
            except OSError as e:
                # May run into permission issues etc.
                continue
    return None, None
