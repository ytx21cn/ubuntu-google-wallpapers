from os.path import basename, splitext
from xml_print import indent_text, generate_xml_element


def get_xml_header():
    """
    The header for the XML files.
    """
    return '<?xml version="1.0" encoding="UTF-8"?>\n'\
           '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'


class Wallpaper:
    """
    Use this class to setup both wallpaper slide show XML and wallpaper images.
    """

    wallpaper_tag = 'wallpaper'

    @classmethod
    def get_wallpaper_title(cls, src_str: str):
        """
        Convert a source string to the title format.
        - Convert all underscores to spaces.
        - Compress consecutive spaces.
        - Remove leading and trailing whitespaces.
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

    def __init__(self, filename, name=None):
        self.filename = str(filename).strip()
        if name is not None:
            self.name = self.get_wallpaper_title(name)
        else:
            main_filename = splitext(basename(self.filename))[0]
            self.name = self.get_wallpaper_title(main_filename)
        self.options = 'zoom'

    def generate_xml(self, indent: int = 0):
        wallpaper_info_list = []
        for (key, val) in vars(self).items():
            wallpaper_info_list.append(generate_xml_element(tag=key, content=str(val)))
        generated_text = generate_xml_element(self.wallpaper_tag, content=wallpaper_info_list)
        return indent_text(generated_text, indent=indent)


class WallpaperImage(Wallpaper):
    """
    Use this subclass to add additional tags for images (*.jpg / *.png).
    These tags include:
    - pcolor
    - scolor
    - shade_type
    """
    def __init__(self, filename, name=None):
        super().__init__(filename, name)
        self.pcolor = '#000000'
        self.scolor = '#000000'
        self.shade_type = 'solid'


def get_unix_start_time():
    """
    Get the starting point of Unix time.
    Return the XML markup.
    """

    start_time_items = [('year', 1970), ('month', 1), ('day', 1),
                        ('hour', 0), ('minute', 0), ('second', 0)]

    start_time_xml_list = []
    for (tag, val) in start_time_items:
        start_time_xml_list.append(generate_xml_element(tag, content='%02d' % val))
    return generate_xml_element('starttime', start_time_xml_list)


class Slide:
    """
    Specify the information of current and next images, as well as lasting minutes for each image.
    A single slide involves one single image and transition to the next image.
    """

    def __init__(self, current_slide: str, next_slide: str, transition_interval: int = 30):
        self.current = str(current_slide)
        self.next = str(next_slide)
        self.transition_sec = 5
        self.lasting_sec = int(transition_interval) * 60 - 5

    def generate_static(self, indent: int = 0):
        generated_text = generate_xml_element('static', content=[
            generate_xml_element('duration', content='%.1f' % self.lasting_sec),
            generate_xml_element('file', content=self.current),
        ])
        return indent_text(generated_text, indent=indent)

    def generate_transition(self, indent: int = 0):
        generated_text = generate_xml_element('transition', content=[
            generate_xml_element('duration', content='%.1f' % self.transition_sec),
            generate_xml_element('from', content=self.current),
            generate_xml_element('to', content=self.next),
        ])
        return indent_text(generated_text, indent=indent)
