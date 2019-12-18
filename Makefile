get_images_exec := main_get_images.py

# Usage:
# To build a target for a specific data directory: make <target> data_dir=<data directory name>
# <target> is one of: [all, get_images, clean]

.PHONY: all error_check get_images clean

all: error_check get_images

error_check:
ifndef data_dir
	$(info Usage: make <target> data_dir=<data directory name>)
	$(info <target> is one of: [all, get_images, clean])
	$(error "EXIT")
endif

images_dir := $(data_dir)/images
source_url_filename := source.url
source_url := $(shell head -n 1 "$(data_dir)/$(source_url_filename)")

get_images: error_check
	@echo $(source_url)
	python3 "$(get_images_exec)" "$(source_url)" "$(images_dir)"

clean: error_check
	-rm -r "$(images_dir)"


