from xml_params import get_bg_properties_xml_header, Wallpaper, WallpaperImage
from xml_print import generate_xml_element, print_indented


def test_wallpaper():
    print(get_bg_properties_xml_header())

    sample_xml = Wallpaper('/usr/share/backgrounds/contest/eoan.xml', name='Ubuntu 19.10 Community Wallpapers')
    sample_image = WallpaperImage('/usr/share/backgrounds/Beijling_park_burial_path_by_Mattias_Andersson.jpg')

    root_tag = 'wallpapers'
    inner_content = [sample_xml.generate_xml(), sample_image.generate_xml()]
    print_indented(generate_xml_element(root_tag, content=inner_content))


if __name__ == '__main__':
    test_wallpaper()