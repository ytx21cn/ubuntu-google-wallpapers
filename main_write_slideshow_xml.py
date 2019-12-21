import glob
import sys

from os.path import dirname, basename, expanduser

from utils import get_py_relpath, safe_mkdir, safe_link


home_dir = expanduser('~')
bg_dir = '%s/.local/share/backgrounds' % home_dir
bg_properties_dir = '%s/.local/share/gnome-background-properties' % home_dir


def main():
    # check command line arguments
    assert len(sys.argv) >= 2,\
        'Usage: python3 %s <images directory>' % get_py_relpath(__file__)

    # get list of images
    images_dir = sys.argv[1]
    images_list = []
    for ext in ['jpg', 'png']:
        images_list += glob.glob('%s/*.%s' % (images_dir, ext))

    # make hard links in designated directory
    collection_name = basename(dirname(images_dir))
    target_dir = '%s/%s' % (bg_dir, collection_name)
    safe_mkdir(target_dir)
    for image in images_list:
        target_image = '%s/%s' % (target_dir, basename(image))
        safe_link(image, target_image)

    # TODO: generate slideshow XML


    # TODO: generate background properties XML

    pass


if __name__ == '__main__':
    main()
