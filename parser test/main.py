import sys
from utils import safe_remove, get_py_relpath, download_html_page
from img_parser import get_images_info


def main():
    assert len(sys.argv) >= 2, '\n[Usage] python3 %s <URL to download>' % get_py_relpath(__file__)

    # get the url to download from using sys.argv[1], and download the page
    # exit if failed to download
    source_url = sys.argv[1]
    source_html_filename = download_html_page(source_url)

    # get images
    images_info = get_images_info(source_html_filename)
    print('Images to download: ')
    for image_info in images_info:
        print(vars(image_info))

    # remove the downloaded html
    safe_remove(source_html_filename)

    # TODO: download image files


if __name__ == '__main__':
    main()
