from html.parser import HTMLParser

# HTML image parser
# parse all <img> tags in an HTML file


class Image:
    def __init__(self, attrs):
        """
        Initialize a image using @attrs
        where @attrs comes from HTMLParser.handle_starttag(tag, attrs)
        """
        attrs_dict = dict(attrs)
        self.src = None if 'src' not in attrs_dict else attrs_dict['src']
        self.alt = None if 'src' not in attrs_dict else attrs_dict['alt']


class ImgParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []

    def handle_starttag(self, tag, attrs):
        """
        Called on calling ImgParser.feed()
        We only handle <img ... /> tags in this parser
        """
        if tag == 'img':
            new_image = Image(attrs)
            self.images.append(new_image)


def get_images(html_file_name):
    with open(html_file_name) as source:
        source_content = source.read()
        parser = ImgParser()
        parser.feed(source_content)
        return parser.images

