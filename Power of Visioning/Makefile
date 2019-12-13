source := https://design.google/library/youtube-visioning/
images_dir := ./images

.PHONY: get_images
get_images:
	$(MAKE) get_images -C .. source="$(source)" images_dir="$(abspath $(images_dir))"

.PHONY: clean
clean:
	rm -r $(images_dir)
