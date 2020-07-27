from sys import stdout


def indent_text(text: str, indent: int = 0) -> str:
    """
    Indent some text by certain levels.
    :param text: the text to be indented (may span over multiple lines).
    :param indent: the level to be indented.
    :return: the indented text as a string.
    """
    result = ''
    indent = int(indent)
    for line in str(text).splitlines():
        result += '%s%s\n' % ('\t' * indent, line)
    return result.rstrip()


def print_indented(text: str, indent: int = 0, file=stdout):
    """
    Print indented text into specified file.
    :param text: the text to be printed.
    :param indent: the indent level.
    :param file: the file DESCRIPTOR for receiving the output.
    """
    print(indent_text(str(text), int(indent)), file=file)


def generate_xml_element(tag: str, content: str or list = None,
                         attrs: dict = {}, block: bool = False,
                         indent: int = 0) -> str:
    """
    Generate an XML element.
    :param tag: XML tag.
    :param content: text content.
    :param attrs: attributes of the XML tag.
    :param block: whether to use block output (i.e. putting text in lines between starting and closing tags).
        - For single-line text only.
    :param indent: indentation level.
    :return: the generated string.
    """

    tag = str(tag)

    # do nothing if there is no valid tag
    if not tag:
        return ''

    # get attributes string
    def list_attrs():
        list_result = ''
        for (key, val) in attrs.items():
            list_result += ' %s="%s"' % (key, val)
        return list_result.strip()

    attrs_str = list_attrs()

    # determine if the content should be generated as block
    # empty content
    if not content:
        content = ''
        block = False
    # multiple lines of content
    elif type(content) is list:
        if len(content) == 0:
            content = ''
        else:
            content = '\n'.join([item for item in content if item])
        block = bool(content)
    # a single line of content
    # keep block settings from argument
    else:
        content = str(content)
        if not content:
            block = False

    # determine indent
    indent = int(indent)

    # handle self-closing tags
    # always create inline output
    if not content:
        if attrs_str:
            result = '<%s %s />' % (tag, attrs_str)
        else:
            result = '<%s />' % tag
        return indent_text(result, indent)

    # handle normal tags
    else:
        if attrs_str:
            tag_open = '<%s %s>' % (tag, attrs_str)
        else:
            tag_open = '<%s>' % tag
        tag_close = '</%s>' % tag

        # inline output
        if not block:
            content = ' '.join(content.splitlines()).strip()
            result = '%s%s%s' % (tag_open, content, tag_close)
        # block output
        else:
            content_lines = [line for line in content.splitlines()
                             if line]  # omit empty lines
            content = '\n'.join(content_lines)
            result = '%s\n%s\n%s' % (tag_open, indent_text(content, indent=1), tag_close)
        return indent_text(result, indent)


def generate_xml_comment(content: str, indent: int = 0):
    """
    Generates an XML comment.
    :param content: the content of the comment
    :param indent: indent level
    :return: the generated comment string with markup.
    """
    content = str(content).strip()
    result = '<!-- %s -->' % content
    return indent_text(result, indent)
