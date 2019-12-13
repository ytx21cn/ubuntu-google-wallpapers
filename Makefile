get_images_exec = main_get_images.py

# This Makefile is not intended to be called directly.
# Instead, one shall create a Makefile in a sub-directory to specify $source and $images_dir, and call this Makefile

.PHONY: get_images
get_images:
	# need to specify source and images_dir
	python3 "$(get_images_exec)" "$(source)" "$(images_dir)"

.PHONY: clean
clean:
	rm -r "$(images_dir)"
