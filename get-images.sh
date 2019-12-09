page_name="index.html"
source="https://design.google/library/youtube-visioning/"
dest_dir="images"

rm -r "./$dest_dir"
mkdir -p "./$dest_dir"

wget -O "$page_name" "$source"

# first command grep: select all images represented by <img /> tags
	# E: extended regular expression; i: case insensitive; n: show line numbers
# second command sed: extract the "src" attribute value of each <img /> tag
	# E: extended regular expression
	# .*: zero or multiple arbitrary characters
	# [^"]*: any character not a double quote character, repeated 0 or more times
	# (): capturing group
# third command wget: get all images using their URLs
	# -i -: specify input tile to be stdin
	# -P: download to given directory
grep -Ein ".*<img.*src=\".*" "$page_name" | sed -E 's/.*<img.*src="([^"]*)".*>/\1/' | wget -i - -P "./$dest_dir"
