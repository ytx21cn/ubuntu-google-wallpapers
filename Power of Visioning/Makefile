source := https://design.google/library/youtube-visioning/
images_dir := $(abspath ./images)

.PHONY: get_images
get_images:
	$(MAKE) get_images -C .. source="$(source)" images_dir="$(images_dir)"

.PHONY: clean
clean:
	$(MAKE) clean -C .. images_dir="$(images_dir)"
