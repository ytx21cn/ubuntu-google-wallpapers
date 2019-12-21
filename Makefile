# Usage:
# To build a target for a specific data directory: make <target> data_dir=<data directory name>

get_images_exec := main_get_images.py
write_xml_exec := main_write_xml.py

bg_dir := $$HOME/.local/share/backgrounds
bg_properties_dir := $$HOME/.local/share/gnome-background-properties


.PHONY: all error_check get_images write_xml clean clean_downloaded clean_generated_bg

all: get_images write_xml

error_check:
ifndef data_dir
	$(info Usage: make <target> data_dir=<data directory name>)
	$(info Use TAB to see the list of available targets)
	$(error "EXIT")
endif

images_dir := $(data_dir)/images
collection_name := $(shell basename "$(data_dir)")
source_url_filename := source.url
source_url := $(shell head -n 1 "$(data_dir)/$(source_url_filename)")

get_images: error_check
	python3 "$(get_images_exec)" "$(source_url)" "$(images_dir)"

write_xml: error_check
	python3 "$(write_xml_exec)" "$(data_dir)"

clean: clean_downloaded clean_generated_bg

clean_downloaded: error_check
	-rm -r "$(images_dir)"

clean_generated_bg: error_check
	-rm -r "$(bg_dir)/$(collection_name)"
	-rm -r "$(bg_properties_dir)/$(collection_name).xml"



