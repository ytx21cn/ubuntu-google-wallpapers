import os, subprocess as sp
from os.path import relpath, dirname, basename
from tempfile import TemporaryDirectory as TD
from sys import stderr


def safe_remove(path: str):
    try:
        os.remove(str(path))
    except:
        pass


def safe_mkdir(dirname):
    os.makedirs(str(dirname), exist_ok=True)


def get_py_relpath(py_file):
    return relpath(py_file, '.')


# TODO: add a support for target directory
def download_from_url(url: str, output_doc: str = None, target_dir: str = None):
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
            output_doc = str(output_doc)

            if target_dir:
                target_dir = str(target_dir)
                safe_mkdir(target_dir)
                output_doc = '%s/%s' % (target_dir, basename(output_doc))
            else:
                safe_mkdir(dirname(output_doc))

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


if __name__ == '__main__':
    source_pic = 'https://storage.googleapis.com/gd-wagtail-prod-assets/images/001_PowerOfVisioning_Hero_2.max-4000x2000.jpegquality-90.png'

    test_results = [
        download_from_url(source_pic),
        download_from_url(source_pic, target_dir='./2'),
        download_from_url(source_pic, output_doc='./3/3.png'),
        download_from_url(source_pic, output_doc='./4a/4.png', target_dir='./4b/'),
    ]
    for i in test_results:
        print(i)

