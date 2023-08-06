# utilities.py

import gzip
import bz2


def open_by_suffix(file_name, mode='r'):
    """
    Open file based on suffix.
    """
    file_name = str(file_name)

    if file_name.endswith('gz'):
        handle = gzip.open(filename=file_name, mode=mode + 't')
    elif file_name.endswith('bz2'):
        handle = bz2.open(filename=file_name, mode=mode + 't')
    else:
        handle = open(file=file_name, mode=mode)

    return handle


def open_by_magic(file_name):
    """
    Open file based on magic.
    """
    magic_dict = {
        '\x1f\x8b\x08': (gzip.open, 'rb'),
        '\x42\x5a\x68': (bz2.BZ2File, 'r')
    }

    max_len = max(len(x) for x in magic_dict)

    with open(file=file_name) as f:
        file_start = f.read(max_len)

    for magic, (fn, flag) in magic_dict.items():
        if file_start.startswith(magic):
            return fn(file_name, flag)

    return open(file_name, mode='r')
