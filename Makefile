# Usage:
# To build a target for a specific data directory: make <target> collection_dir=<collection directory name> transition_interval=<number of minutes, int <= 1440>

get_images_exec := main_get_images.py
write_xml_exec := main_write_xml.py

bg_dir := $$HOME/.local/share/backgrounds
bg_properties_dir := $$HOME/.local/share/gnome-background-properties

.PHONY: all
all: get_images write_xml

# check error (this shall be done before doing anything using Makefile)
.PHONY: error_check
error_check:
ifndef collection_dir
	$(info Usage: make <target> collection_dir=<collection directory name> transition_interval=<number of minutes, int <= 1440>)
	$(info Use TAB to see the list of available targets)
	$(error "EXIT")
endif

images_dir := $(collection_dir)/images
collection_name := $(shell basename "$(collection_dir)")
source_url_filename := source.url
source_url := $(shell head -n 1 "$(collection_dir)/$(source_url_filename)")

# get images from a specified source URL
# and save it to the specified directory
.PHONY: get_images
get_images: error_check
	python3 "$(get_images_exec)" "$(source_url)" "$(images_dir)"

# write the XMget_imagesL files for wallpaper slideshow
# using specified image directory and transition interval
.PHONY: write_xml
write_xml: error_check
	python3 "$(write_xml_exec)" "$(collection_dir)" "$(transition_interval)"

# clean up
.PHONY: clean
clean: clean_downloaded clean_generated_bg

# clean up downloaded images
# (this does NOT affect images shown in System Settings)
.PHONY: clean_downloaded
clean_downloaded: error_check
	-rm -r "$(images_dir)"

# clean up slide show files
# and remove settings from the System Settings UI
.PHONY: clean_generated_bg
clean_generated_bg: error_check
	-rm -r "$(bg_dir)/$(collection_name)"
	-rm -r "$(bg_properties_dir)/$(collection_name).xml"



