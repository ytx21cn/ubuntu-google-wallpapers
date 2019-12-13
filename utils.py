import os, subprocess as sp
from os.path import relpath, dirname, basename
from tempfile import TemporaryDirectory as TD
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except:
        pass


def safe_mkdir(path: str):
    os.makedirs(str(path), exist_ok=True)


def get_py_relpath(py_file):
    return relpath(py_file, '.')
