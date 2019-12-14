import os
import subprocess as sp
from sys import stderr

from os.path import basename, dirname, relpath
from tempfile import TemporaryDirectory
from utils import safe_mkdir


def download_from_url(url: str, output_doc: str = None, target_dir: str = None, exit_on_error: bool = False):
    """
    Using wget to download the specified @source_url.
    Output rules:
        1. If @output_doc and @target_dir are both not specified, then download to current directory
        2. If @output_doc is specified but @target_dir is not specified, then download to the path of @output_doc
        3. If @output_doc is not specified but @target_dir is specified, then download to the directory @target_dir
        4. If @output_doc and @target_dir are both specified, then only keep the basename of @output_doc, but download to the directory @target_dir
    If @output_doc or @target_dir indicates a directory that does not exist yet, it will be created.
    Return the downloaded filename.
    If @source_url downloading fails, then exit the process immediately.
    """

    def wget_helper(wget_args: list):
        """
        Helper: download the specified @url in parent function using @wget_args
        If failed to download, check if @exit_on_error is True
            - If True: exit
            - Otherwise: return False
        If succeeded to download, return True
        """
        wget_exit_code = sp.call(wget_args)
        if wget_exit_code != 0:
            print('ERROR: failed to download %s\n' % url, file=stderr)
            if exit_on_error:
                exit(-1)
            else:
                return False
        print('Successfully downloaded: %s\n' % url, file=stderr)
        return True

    # handle the downloading in temporary directory
    with TemporaryDirectory() as temp_dir:
        # download the requested file from @url
        wget_args = ['wget', url]
        if output_doc:
            temp_output_doc = '%s/%s' % (temp_dir, basename(str(output_doc)))
            wget_args += ['-O', temp_output_doc]
        else:
            wget_args += ['-P', temp_dir]
        download_succeeded = wget_helper(wget_args)

        if not download_succeeded:
            if exit_on_error:
                exit(-1)
            else:
                return None

        # at this point wget_helper() should have gathered file
        # now move the file in temporary directory to actual directory
        mv_args = ['mv', '-v']

        if output_doc:
            output_doc = str(output_doc)

            if target_dir:
                target_dir = str(target_dir)
                safe_mkdir(target_dir)
                output_doc = '%s/%s' % (target_dir, basename(output_doc))
            else:
                safe_mkdir(dirname(output_doc) or '.')

            mv_args += [temp_output_doc, output_doc]

        else:
            target_dir = str(target_dir) if target_dir else '.'
            safe_mkdir(target_dir)

            downloaded_filename = os.listdir(temp_dir)[0]
            downloaded_file_path = '%s/%s' % (temp_dir, downloaded_filename)

            output_doc = '%s/%s' % (target_dir, downloaded_filename)

            mv_args += [downloaded_file_path, output_doc]

        sp.call(mv_args)
        return relpath(str(output_doc), '.')
