import os
from os.path import abspath
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except OSError:
        pass


def safe_mkdir(path: str):
    os.makedirs(str(path), exist_ok=True)


def safe_link(src: str, dest: str):
    src = abspath(str(src))
    dest = abspath(str(dest))
    try:
        os.link(src, dest)
        print('[Hard link created]\nFROM: %s\nTO: %s' % (src, dest), file=stderr)
    except OSError:
        print('[File exists]\n%s' % dest, file=stderr)
