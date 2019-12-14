import sys
from utils import safe_mkdir, safe_remove, get_py_relpath
from download import download_from_url
from img_parser import get_images_info


def main():
    # check command line arguments
    assert len(sys.argv) >= 2,\
        '\n[Usage] python3 %s <URL to download>' \
        '[directory to save images]' % get_py_relpath(__file__)

    # get the URL to download from using command line argument, and download the page
    # exit if failed to download
    source_url = sys.argv[1]
    source_html_filename = download_from_url(source_url, output_doc='index.html', exit_on_error=True)

    # get images URL and their descriptions
    images_info = get_images_info(source_html_filename)
    num_total_images = len(images_info)
    print('%s image(s) to download: ' % num_total_images)
    index = 0
    for image_info in images_info:
        index += 1
        print('[%s] %s' % (index, vars(image_info)))

    # remove the downloaded html
    safe_remove(source_html_filename)

    # download images
    target_dir = str(sys.argv[2]) if len(sys.argv) >= 3 else '.'
    safe_mkdir(target_dir)
    index = 0
    num_success = 0
    num_failure = 0
    for image_info in images_info:
        index += 1
        print('Downloading image %s of %s' % (index, num_total_images))
        downloaded_filename = download_from_url(image_info.src, target_dir=target_dir)
        if downloaded_filename is not None:
            num_success += 1
            print('[Download success: %s / %s]\n%s' % (num_success, num_total_images, downloaded_filename))
        else:
            num_failure += 1
            print('[Download failed: %s / %s]\n%s' % (num_failure, num_total_images, image_info.src))

    # print final results
    print('[Download results]')
    print('Success: %s / %s' % (num_success, num_total_images))
    print('Failure: %s / %s' % (num_failure, num_total_images))


if __name__ == '__main__':
    main()
