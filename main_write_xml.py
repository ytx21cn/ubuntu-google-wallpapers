import glob
import sys
from os.path import abspath, basename, expanduser, isdir
from sys import stderr

from utils import get_py_relpath, safe_mkdir, safe_link
from xml_params import get_bg_properties_xml_header, get_unix_start_time, Wallpaper, WallpaperImage, Slide
from xml_print import generate_xml_element, generate_xml_comment
from img_parser import image_exts

bg_dir = expanduser('~/.local/share/backgrounds')
bg_properties_dir = expanduser('~/.local/share/gnome-background-properties')
for i in [bg_dir, bg_properties_dir]:
    safe_mkdir(i)

images_dir_name = 'images'


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
    # default is 30 minutes
    min_per_day = 24 * 60
    if len(sys.argv) >= 3:
        try:
            transition_interval = min(int(sys.argv[2]), min_per_day)
        except ValueError:
            transition_interval = 30

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
        """
        Generate a slide show XML.
        Put the XML into "~/.local/share/backgrounds" directory.
        """

        root_tag = 'background'

        # start time
        start_time = get_unix_start_time()
        start_time_comment = generate_xml_comment('This animation starts at the beginning of the unix epoch.')

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

        # combine together into XML
        combined_xml = generate_xml_element(tag=root_tag, content=[
            start_time,
            start_time_comment,
            *slides_xml_list
        ])
        return combined_xml

    # write slide show XML to file
    slide_show_xml_filename = abspath('%s/%s.xml' % (target_dir, basename(target_dir)))
    with open(slide_show_xml_filename, 'w') as slide_show_file:
        print(generate_slide_show_xml(), file=slide_show_file)
        print('[Generated slide show XML file]\n%s' % slide_show_xml_filename, file=stderr)

    # generate background properties XML
    def generate_bg_properties_xml():
        """
        Generate a background properties XML.
        Put the XML into "~/.local/share/gnome-background-properties" directory.
        """

        root_tag = 'wallpapers'
        item_tag = 'wallpaper'
        bg_list = []

        # first add slide show XML
        slide_show = Wallpaper(slide_show_xml_filename, name=collection_name)
        slide_show_xml_element = slide_show.generate_xml()
        bg_list.append(slide_show_xml_element)

        # then add images
        for image_filename in linked_images:
            image = WallpaperImage(image_filename)
            image_xml_element = image.generate_xml()
            bg_list.append(image_xml_element)

        # combine together into XML
        combined_xml = generate_xml_element(tag=root_tag, content=bg_list)
        return combined_xml

    # write background properties XML to file
    bg_properties_xml_filename = abspath('%s/%s.xml' % (bg_properties_dir, collection_name))
    with open(bg_properties_xml_filename, 'w') as bg_properties_file:
        header = get_bg_properties_xml_header()
        print(header, file=bg_properties_file)
        print(generate_bg_properties_xml(), file=bg_properties_file)
        print('[Generated background properties XML file]\n%s' % bg_properties_xml_filename, file=stderr)


if __name__ == '__main__':
    main()
