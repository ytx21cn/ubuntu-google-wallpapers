from os.path import basename, splitext
from xml_print import indent_text, print_indented, generate_xml_element
from collections import OrderedDict


bg_properties_xml_header = \
    '<?xml version="1.0" encoding="UTF-8"?>\n'\
    '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'


class Wallpaper:
    """
    Use this class to setup both wallpaper slide show XML and wallpaper images
    """

    def __init__(self, filename, name=None):

        def normalize(src_str: str):
            """
            Normalize a @src_str so that it is appropriate to be used as a title
            """

            # remove leading and trailing whitespaces
            result_str = str(src_str).strip()
            # convert all underscores ('_') to spaces
            # and also compress consecutive underscores / spaces into one space
            # then remove leading and trailing whitespaces
            result_str = ' '.join([i for i in result_str.split('_') if i]).strip()
            result_str = ' '.join([i for i in result_str.split(' ') if i]).strip()
            # convert to title case
            result_str = result_str.title()

            return result_str

        self.filename = str(filename).strip()
        if name is not None:
            self.name = normalize(name)
        else:
            main_filename = splitext(basename(self.filename))[0]
            self.name = normalize(main_filename)
        self.options = 'zoom'

    def generate_xml(self, indent: int = 0):
        wallpaper_info_list = []
        for (key, val) in vars(self).items():
            wallpaper_info_list.append(generate_xml_element(tag=key, content=str(val)))
        generated_text = generate_xml_element('wallpaper', content=wallpaper_info_list)
        return indent_text(generated_text, indent=indent)


class WallpaperImage(Wallpaper):
    """
    Use this subclass to add additional attributes for images (*.jpg / *.png)
    """

    def __init__(self, filename, name=None):
        super().__init__(filename, name)
        self.pcolor = '#000000'
        self.scolor = '#000000'
        self.shade_type = 'solid'


def test_wallpaper():
    sample_xml = Wallpaper('/usr/share/backgrounds/contest/eoan.xml', name='Ubuntu 19.10 Community Wallpapers')
    sample_image = WallpaperImage('/usr/share/backgrounds/Beijling_park_burial_path_by_Mattias_Andersson.jpg')

    root_tag = 'wallpapers'
    inner_tag = 'wallpaper'
    inner_content = [sample_xml.generate_xml(), sample_image.generate_xml()]
    print_indented(generate_xml_element(root_tag, content=inner_content))


def get_unix_start_time():
    starttime_dict = OrderedDict([
        ('year', '1970'),
        ('month', '01'),
        ('day', '01'),
        ('hour', '00'),
        ('minute', '00'),
        ('second', '00'),
    ])

    starttime_xml_list = []
    for (key, val) in starttime_dict.items():
        starttime_xml_list.append(generate_xml_element(key, content=val))
    return generate_xml_element('starttime', starttime_xml_list)



if __name__ == '__main__':
    print(bg_properties_xml_header)
    test_wallpaper()
    print_indented(get_unix_start_time())
