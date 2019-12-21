import os
from os.path import relpath, abspath
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except:
        pass


def safe_mkdir(path: str):
    os.makedirs(str(path), exist_ok=True)


def safe_link(src: str, dest: str):
    src = str(src)
    dest = str(dest)
    try:
        os.link(src, dest)
        print('Hard link created: %s -> %s' % (abspath(src), abspath(dest)), file=stderr)
    except:
        pass


def get_py_relpath(py_file):
    return relpath(py_file, '.')
