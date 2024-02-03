# HDRItoSkybox

Convert HDRI images into six-image skyboxes, using the python cv2 library

## Usage

`python convert.py path/to/hdri path/to/output [--brightness-scale=1]`

Example: `python convert.py images/hochsal_field_1k.hdr ~/.minetest/mods/hdriskybox/textures/test`

Note: make sure that the output path is not a full image path. Leave it at something like `textures/skybox`, and the program will save the images to `textures/skybox_top.png`, `textures/skybox_front.png`, and so on.

The optional parameter scales the brightness of the output images. By default, the brightness of the output images are scaled so that 255 is the average brightness of the original HDRI. This is done since many HDRI's are quite dim in most places. Ideally, this would be corrected by using a tonemap or something, but I do not currently have the time or expertise to implement that.