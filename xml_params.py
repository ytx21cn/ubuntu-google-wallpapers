from os.path import basename, splitext
from sys import stdout
from xml_print import print_indented


xml_header = \
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

    def print(self, indent: int = 0, file=stdout):
        print_indented('<wallpaper>', indent=indent, file=file)
        for (key, val) in vars(self).items():
            print_indented('<%s>%s</%s>' % (key, val, key), indent=indent+1, file=file)
        print_indented('</wallpaper>', indent=indent, file=file)


class WallpaperImage(Wallpaper):
    """
    Use this subclass to add additional attributes for images (*.jpg / *.png)
    """

    def __init__(self, filename, name=None):
        super().__init__(filename, name)
        self.pcolor = '#000000'
        self.scolor = '#000000'
        self.shade_type = 'solid'


if __name__ == '__main__':
    sample_image = WallpaperImage('/usr/share/backgrounds/Beijling_park_burial_path_by_Mattias_Andersson.jpg')
    sample_image.print(indent=1)
