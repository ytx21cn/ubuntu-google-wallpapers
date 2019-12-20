from os.path import basename, splitext
from xml_print import indent_text, generate_xml_element


def get_bg_properties_xml_header():
    return \
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
            - Convert all underscores to spaces
            - Compress consecutive spaces
            - Remove leading and trailing whitespaces
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


def get_unix_start_time():
    """
    Get the starting point of Unix time
    Return the XML markup
    """

    starttime_items = [
        ('year', 1970),
        ('month', 1),
        ('day', 1),
        ('hour', 0),
        ('minute', 0),
        ('second', 0),
    ]

    starttime_xml_list = []
    for (tag, val) in starttime_items:
        starttime_xml_list.append(generate_xml_element(tag, content='%02d' % val))
    return generate_xml_element('starttime', starttime_xml_list)


class Slide:
    """
    Specify the information of current and next images, as well as lasting minutes for each image
    """
    def __init__(self, current: str, next: str, lasting_min: int = 30):
        self.current = str(current)
        self.next = str(next)
        self.transition_sec = 5
        self.lasting_sec = int(lasting_min) * 60 - 5

    def generate_static(self, indent: int = 0):
        generated_text = generate_xml_element('static', content=[
            generate_xml_element('duration', content='%.1f' % self.lasting_sec),
            generate_xml_element('file', content=self.current),
        ])
        return indent_text(generated_text, indent=indent)

    def generate_transition(self, indent: int = 0):
        generated_text = generate_xml_element('transition', content=[
            generate_xml_element('duration', content='%.1f' % self.lasting_sec),
            generate_xml_element('from', content=self.current),
            generate_xml_element('to', content=self.next),
        ])
        return indent_text(generated_text, indent=indent)
