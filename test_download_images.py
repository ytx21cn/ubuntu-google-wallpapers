from tempfile import TemporaryDirectory
from os.path import dirname

from utils import safe_mkdir
from img_parser import get_images_info
from download import download_from_url


test_data_dir = '%s/test_data' % dirname(__file__)
source_url_file = '%s/test_source.url' % test_data_dir
images_dir = '%s/images' % test_data_dir


def test_download_images():
    # get source URL
    source_url = ''
    with open(source_url_file) as source_file:
        source_url += source_file.read()

    # get images
    with TemporaryDirectory() as temp_dir:
        # get html first
        html_file = '%s/index.html' % temp_dir
        download_from_url(source_url, output_doc=html_file)
        images_info = get_images_info(html_filename=html_file)

        print('Images to download:')
        for (index, image_info) in enumerate(images_info):
            print('[%s] %s' % (index+1, vars(image_info)))

        # get images
        safe_mkdir(images_dir)
        for image_info in images_info:
            download_from_url(image_info.src, target_dir=images_dir)


if __name__ == '__main__':
    test_download_images()
