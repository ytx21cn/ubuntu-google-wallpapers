import os, subprocess as sp
from sys import stderr
from img_parser import get_images


def download_from_source(source_url, output_doc='index.html'):
    wget_exit_code = sp.call(['wget', '-O', output_doc, source_url])
    if wget_exit_code != 0:
        print('ERROR: failed to download %s\n' % source_url, stderr)
        exit(-1)
    print('Successfully downloaded: %s\n', stderr)
    return output_doc


def main():
    # get the url to download from
    source_txt = 'source.txt'
    with open(source_txt) as source:
        source_url = source.read()
    source_html_filename = download_from_source(source_url)

    # get inamges
    images = get_images(source_html_filename)
    for image in images:
        print(vars(image))

    # remove the downloaded html
    try:
        os.remove(source_html_filename)
    except:
        pass


if __name__ == '__main__':
    main()
