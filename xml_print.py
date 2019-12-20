from sys import stdout


def indent_text(text: str, indent: int = 0):
    result = ''
    indent = int(indent)
    for line in str(text).splitlines():
        result += '%s%s\n' % ('\t' * indent, line)
    return result.rstrip()


def print_indented(text: str, indent: int = 0, file=stdout):
    print(indent_text(str(text), int(indent)), file=file)


def generate_xml_element(tag: str, content: str or list = None, attrs: dict = None, block=False, indent: int = 0):
    tag = str(tag)
    # do nothing without a valid tag
    if not tag:
        return

    attrs = dict(attrs) if attrs else {}

    def list_attrs():
        list_result = ''
        for (key, val) in attrs.items():
            list_result += ' %s="%s"' % (key, val)
        return list_result.strip()
    attrs_str = list_attrs()

    if not content:
        content = None
        block = False
    elif type(content) is list:
        content = None if len(content) == 0 \
            else '\n'.join([item for item in content if item])
        block = bool(content)
    else:
        content = str(content)
        if not content:
            block = False

    indent = int(indent)

    # handle self-closing tags
    # always create inline output
    if not content:
        result = '<%s %s />' % (tag, attrs_str) if attrs_str \
            else ('<%s />' % tag)
        return indent_text(result, indent)

    # handle normal tags
    else:
        tag_open = '<%s %s>' % (tag, attrs_str) if attrs_str \
            else ('<%s>' % tag)
        tag_close = '</%s>' % tag

        # inline output
        if not block:
            content = ' '.join(content.splitlines()).strip()
            result = '%s%s%s' % (tag_open, content, tag_close)
        # block output
        else:
            content_lines = [line for line in content.splitlines() if line]
            content = '\n'.join(content_lines)
            result = '%s\n%s\n%s' % (tag_open, indent_text(content, indent=1), tag_close)

        return indent_text(result, indent)


def xml_print_test():
    tag_outer = 'outer'
    attrs_outer = {'x': 1, 'y': 2}
    text1 = 'The quick brown fox jumps over the lazy dog.'

    tag_inner = 'inner'
    text2 = 'I love Python!'

    def test_single_tag():
        print(generate_xml_element(tag_outer))

    def test_single_tag_with_attrs():
        print(generate_xml_element(tag_outer, attrs=attrs_outer))

    def test_single_tag_inline():
        print(generate_xml_element(tag_outer, content=text1))

    def test_single_tag_attrs_block():
        print(generate_xml_element(tag_outer, attrs=attrs_outer, content=text1, block=True))

    def test_multiline():
        multiline_content = [text1, text2]
        print(generate_xml_element(tag_outer, attrs=attrs_outer, content=multiline_content, block=True))

    def test_nested():
        nested_content = [text1, generate_xml_element(tag_inner, content=text2)]
        print(generate_xml_element(tag_outer, content=nested_content, block=True))

    def test_nested_blocks():
        nested_content = [text1, generate_xml_element(tag_inner, content=text2, block=True)]
        print(generate_xml_element(tag_outer, attrs=attrs_outer, content=nested_content, block=True))

    test_single_tag()
    test_single_tag_with_attrs()
    test_single_tag_inline()
    test_single_tag_attrs_block()
    test_multiline()
    test_nested()
    test_nested_blocks()

if __name__ == '__main__':
    xml_print_test()
