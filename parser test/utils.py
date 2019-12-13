import os, subprocess as sp
from os.path import relpath, basename
from tempfile import TemporaryDirectory as TD
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except:
        pass


def get_py_relpath(py_file):
    return relpath(py_file, '.')


# TODO: add a support for target directory
def download_from_url(url: str, output_doc: str = None, target_dir: str = '.'):
    """
    Using wget to download the specified @source_url
    Return the downloaded filename
    If @source_url downloading fails, then exit the process immediately
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
    with TD() as temp_dir:
        # download
        wget_args = ['wget', url]
        if output_doc:
            temp_output_doc = '%s/%s' % (temp_dir, basename(str(output_doc)))
            wget_args += ['-O', temp_output_doc]
        else:
            wget_args += ['-P', temp_dir]
        wget_helper(wget_args)

        # at this point wget_helper() should have successfully got the file
        # otherwise the process should have already exited
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


if __name__ == '__main__':
    download_from_url('https://storage.googleapis.com/gd-wagtail-prod-assets/images/001_PowerOfVisioning_Hero_2.max-4000x2000.jpegquality-90.png');
