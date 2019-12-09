page_name="index.html"
source="https://design.google/library/youtube-visioning/"
dest_dir="images"

wget -O "$page_name" "$source"
wget_exit_code=$?
# error checking: make sure that the webpage is obtained
if [ $wget_exit_code -ne 0 ]
then
	rm "$page_name"
	echo -e "ERROR: failed to get $source\nNow exiting."
	exit
fi

rm -r "./$dest_dir"
mkdir -p "./$dest_dir"


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

rm "$page_name"
