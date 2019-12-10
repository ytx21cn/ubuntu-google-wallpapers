import os, subprocess as sp
from sys import stderr
from img_parser import get_images_info


def download_html_page(source_url, output_doc='index.html'):
    wget_exit_code = sp.call(['wget', '-O', str(output_doc), str(source_url)])
    if wget_exit_code != 0:
        print('ERROR: failed to download %s\n' % source_url, file=stderr)
        exit(-1)
    print('Successfully downloaded: %s\n' % source_url, file=stderr)
    return output_doc


def main():
    # get the url to download from
    url_container_path = 'source.txt'
    with open(url_container_path) as url_container:
        source_url = url_container.read()
    source_html_filename = download_html_page(source_url)

    # get images
    images = get_images_info(source_html_filename)
    for image in images:
        print(vars(image))

    # remove the downloaded html
    try:
        os.remove(source_html_filename)
    except:
        pass


if __name__ == '__main__':
    main()
