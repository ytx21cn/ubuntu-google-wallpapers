# Ubuntu Google wallpapers
Download wallpapers from [Google Design](https://design.google) and use them for system slideshows.

## Usage
### Download images from server, and put them into System Settings
* Example: `make all collection_dir=collections/Design\ is\ Never\ Done/ transition_interval=30`
* Replace `collection_dir` and `transition_interval` values as you wish.
* `transition_interval` is in the unit of minutes, and it shall be not greater than 1440 (the number of minutes in a day).

### Remove images from System Settings
* Example: `make clean collection_dir=collections/Design\ is\ Never\ Done/`
* Replace `collection_dir` as you wish.
