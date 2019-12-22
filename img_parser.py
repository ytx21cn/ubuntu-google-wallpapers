from html.parser import HTMLParser
from os.path import splitext

# HTML image parser
# parse all <img> tags in an HTML file

image_exts = ['jpg', 'png']


class ImageInfo:
    def __init__(self, attrs):
        """
        Initialize the information of a image using @attrs
        where @attrs comes from HTMLParser.handle_starttag(tag, attrs)
        """
        attrs_dict = dict(attrs)
        self.src = None if 'src' not in attrs_dict else attrs_dict['src']
        self.alt = None if 'src' not in attrs_dict else attrs_dict['alt']


class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images_info = []

    def handle_starttag(self, tag, attrs):
        """
        Called on calling ImgParser.feed()
        We only handle <img ... /> tags in this parser
        """
        if tag == 'img':
            new_image_info = ImageInfo(attrs)
            src = new_image_info.src
            if not src:
                pass
            else:
                src_ext = splitext(str(src))[1]
                # exclude starting '.'
                if src_ext[1:] in image_exts:
                    self.images_info.append(new_image_info)


def get_images_info(html_filename: str):
    """
    Using the <img> tags in @html_filename, get information of all images listed in the document
    """
    with open(html_filename) as source:
        source_content = source.read()
        parser = ImgParser()
        parser.feed(source_content)
        return parser.images_info

