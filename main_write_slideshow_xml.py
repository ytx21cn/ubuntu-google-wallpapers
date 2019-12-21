import glob
import sys
from os.path import abspath, basename, expanduser, isdir
from sys import stderr

from utils import get_py_relpath, safe_mkdir, safe_link
from xml_params import get_bg_properties_xml_header, get_unix_start_time, Slide
from xml_print import generate_xml_element, xml_comment

home_dir = expanduser('~')
bg_dir = '%s/.local/share/backgrounds' % home_dir
bg_properties_dir = '%s/.local/share/gnome-background-properties' % home_dir

images_dir_name = 'images'
image_exts = ['jpg', 'png']


def main():
    # check command line arguments
    assert len(sys.argv) >= 2,\
        'Usage: python3 %s <data directory, with sub-directory "%s">'\
        '[transition interval in minutes (default is 30)]'\
        % (get_py_relpath(__file__), images_dir_name)

    # check source images directory
    src_data_dir = sys.argv[1]
    src_images_dir = '%s/%s' % (src_data_dir, images_dir_name)
    if not isdir(src_images_dir):
        raise FileNotFoundError('%s has no sub-directory "%s"' % (src_data_dir, images_dir_name))

    # set transition interval using command line argument
    transition_interval = 30
    if len(sys.argv) >= 3:
        transition_interval = sys.argv[2]

    # get list of images
    images_list = []
    for ext in image_exts:
        images_list += glob.glob('%s/*.%s' % (src_images_dir, ext))

    # make hard links of images in designated directory
    collection_name = basename(abspath('%s/..' % src_images_dir))
    target_dir = '%s/%s' % (bg_dir, collection_name)
    safe_mkdir(target_dir)
    for image in images_list:
        target_image = '%s/%s' % (target_dir, basename(image))
        safe_link(image, target_image)

    linked_images = []
    for ext in image_exts:
        linked_images += glob.glob('%s/*.%s' % (target_dir, ext))
    linked_images.sort()

    # generate slide show XML
    def generate_slide_show_xml():
        root_tag = 'background'

        # start time
        start_time = get_unix_start_time()
        start_time_comment = xml_comment('This animation starts at the beginning of the unix epoch.')

        # slides list
        num_total_images = len(linked_images)
        slides_xml_list = []
        for image_index in range(0, num_total_images):
            # get current and next images
            current_image = abspath(linked_images[image_index])
            next_index = (image_index + 1) % num_total_images
            next_image = abspath(linked_images[next_index])
            # generate XML transition
            new_slide = Slide(current_image, next_image, transition_interval)
            slides_xml_list.append(new_slide.generate_static())
            slides_xml_list.append(new_slide.generate_transition())

        combined_slide_show_xml = generate_xml_element(tag=root_tag, content=[
            start_time,
            start_time_comment,
            *slides_xml_list
        ])
        return combined_slide_show_xml

    slide_show_xml_filename = abspath('%s/%s.xml' % (target_dir, basename(target_dir)))
    with open(slide_show_xml_filename, 'w') as slide_show_file:
        print(generate_slide_show_xml(), file=slide_show_file)
        print('[Generated XML file]\n%s' % slide_show_xml_filename, file=stderr)


    # TODO: generate background properties XML

    pass


if __name__ == '__main__':
    main()
