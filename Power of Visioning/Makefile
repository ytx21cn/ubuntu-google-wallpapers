source := https://design.google/library/youtube-visioning/
get_images_exec := ../get_images.py
images_dir := ./images

.PHONY: get_images
get_images:
	python3 $(get_images_exec) $(source) $(images_dir)

.PHONY: clean
clean:
	rm -r $(images_dir)
