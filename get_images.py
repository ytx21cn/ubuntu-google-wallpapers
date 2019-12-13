import sys
from utils import safe_remove, safe_mkdir, get_py_relpath, download_from_url
from img_parser import get_images_info


def main():
    assert len(sys.argv) >= 2, '\n[Usage] python3 %s <URL to download> [directory to save images]' % get_py_relpath(__file__)

    # get the URL to download from using command line argument, and download the page
    # exit if failed to download
    source_url = sys.argv[1]
    source_html_filename = download_from_url(source_url, output_doc='index.html', exit_on_error=True)

    # get images URL and their descriptions
    images_info = get_images_info(source_html_filename)
    print('%s image(s) to download: ' % len(images_info))
    index = 0
    for image_info in images_info:
        index += 1
        print('[%s] %s' % (index, vars(image_info)))

    # remove the downloaded html
    safe_remove(source_html_filename)

    # download images
    target_dir = str(sys.argv[2]) if len(sys.argv) >= 3 else '.'
    index = 0
    for image_info in images_info:
        index += 1
        print('Downloading image %s of %s' % (index, len(images_info)))
        download_from_url(image_info.src, target_dir=target_dir)


if __name__ == '__main__':
    main()
