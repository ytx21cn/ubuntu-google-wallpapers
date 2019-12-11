import os, subprocess as sp
from os.path import relpath
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except:
        pass


def get_py_relpath(py_file):
    return relpath(py_file, '.')

def download_html_page(source_url: str, output_doc: str = 'index.html'):
    """
    Using wget to download the specified @source_url
    Exit the program immediately if @source_url failed to be downloaded
    """
    wget_exit_code = sp.call(['wget', '-O', str(output_doc), str(source_url)])
    if wget_exit_code != 0:
        print('ERROR: failed to download %s\n' % source_url, file=stderr)
        exit(-1)
    print('Successfully downloaded: %s\n' % source_url, file=stderr)
    return output_doc
