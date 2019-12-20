from xml_print import generate_xml_element


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

