page_name="index.html"
source="https://design.google/library/youtube-visioning/"
dest_dir="images"

rm -r "./$dest_dir"
mkdir -p "./$dest_dir"

wget -O "$page_name" "$source"
grep -Ein ".*<img.*src=\".*" "$page_name" | sed -E 's/.*<img.*src="([^"]*)".*>/\1/' | wget -i - -P "./$dest_dir"
