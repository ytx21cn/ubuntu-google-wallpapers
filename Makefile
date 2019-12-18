get_images_exec := main_get_images.py

# Usage:
# To build a target for a specific data directory: make <target> data_dir=<data directory name>
# <target> is one of: [all, get_images, clean]

DATA_DIR =
ifndef DATA_DIR
$(info Usage: make <target> DATA_DIR=<data directory name>)
$(info <target> is one of: [all, get_images, clean])
$(error "EXIT")
else
images_dir := $(DATA_DIR)/images
source_url_filename := source.url
source_url := $(shell head -n 1 "$(DATA_DIR)/$(source_url_filename)")
endif

.PHONY: all get_images clean

all: get_images


get_images:
	@echo $(source_url)
	python3 "$(get_images_exec)" "$(source_url)" "$(images_dir)"

clean:
	-rm -r "$(images_dir)"


