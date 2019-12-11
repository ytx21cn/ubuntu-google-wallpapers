import os, subprocess as sp
from os.path import relpath, basename
from tempfile import TemporaryDirectory
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except:
        pass


def get_py_relpath(py_file):
    return relpath(py_file, '.')


# TODO: modify this function to download image files
def download_from_url(url: str, output_doc: str = None):
    """
    Using wget to download the specified @source_url
    Return the downloaded filename
    If @source_url failed to be downloaded, then exit the process immediately
    """

    def wget_helper(wget_args: list):
        """
        Helper: download the specified @url in parent function using @wget_args
        If failed to download, then exit the process immediately
        """
        wget_exit_code = sp.call(wget_args)
        if wget_exit_code != 0:
            print('ERROR: failed to download %s\n' % url, file=stderr)
            exit(-1)
        print('Successfully downloaded: %s\n' % url, file=stderr)

    # handle the downloading in temporary directory
    with TemporaryDirectory() as temp_dir:
        # download
        wget_args = ['wget', url]
        if output_doc:
            temp_output_doc = '%s/%s' % (temp_dir, basename(str(output_doc)))
            wget_args += ['-O', temp_output_doc]
        else:
            wget_args += ['-P', temp_dir]
        wget_helper(wget_args)

        # at this point wget_helper() should have successfully got the file
        # otherwise the process has already exited
        # now move the file in temporary directory to actual directory
        mv_args = ['mv']
        if output_doc:
            mv_args += [temp_output_doc, output_doc]
            sp.call(mv_args)
            return output_doc
        else:
            downloaded_filename = os.listdir(temp_dir)[0]
            downloaded_file_path = '%s/%s' % (temp_dir, downloaded_filename)
            mv_args += [downloaded_file_path, './%s' % downloaded_filename]
            sp.call(mv_args)
            return downloaded_filename




