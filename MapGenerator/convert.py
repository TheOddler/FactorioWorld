import os, sys
import math
from PIL import Image
from tqdm import tqdm
from helpers import *

# Settings
image_file = 'NE2_LR_LC_SR_W_DR.tif' #change me for different image
resize_width = 8064 # Number (ex 500) or None

terrain_codes = [
    #((0,0,0), "_", "out-of-map"), #commented out those I don't want to generate
    ((89,140,182), "o", "deepwater"), #ocean
    #((24,39,14), "O", "deepwater-green"),
    ((114,173,213), "w", "water"),
    #((30,48,16), "W", "water-green"),
    ((145,190,148), "g", "grass-1"),
    ((180,205,165), "m", "grass-3"),
    ((212,218,174), "G", "grass-2"),
    ((220,220,217), "d", "dirt-3"),
    ((154,149,135), "D", "dirt-6"),
    ((241,237,209), "s", "sand-1"),
    ((227,203,188), "S", "sand-3")
]


# Maybe settings
# The controller of the mod assumes the world files are name "World_large" and "World_small", so if you change this, make sure to rename the files later too or change the name in control.lua
output_file_prefix = 'World' #change me for a different output file




## Only change stuff below here when you know what you're doing, or like to live dangerously.

# Globals
Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
image_file = os.path.join(sys.path[0], image_file)
print(f"Loading image...")
image = Image.open(image_file).convert('RGB') # the image to use

output_file_path_partial = os.path.join(sys.path[0], output_file_prefix)

# Optionally resize image
if resize_width:
    width, height = image.size
    resize_height = int(float(height)*float(resize_width / float(width)))
    print(f"Resizing image from {width}, {height} to {resize_width}, {resize_height}...")
    large_image = image.resize((resize_width, resize_height), Image.LANCZOS)
else:
    large_image = image

# Make half-size image for the small map
width, height = large_image.size
small_width = int(width / 2)
small_height = int(height / 2)
print(f"Creating small image with size {small_width}, {small_height}...")
small_image = image.resize((small_width, small_height), Image.LANCZOS)

def get_terrain_letter(pixel):
    min_dist = float("inf")
    found_code = None
    for color, code, _ in terrain_codes:
        dist = color_color_distance(pixel, color)
        if dist < min_dist:
            min_dist = dist
            found_code = code
    return found_code

# Line converts
def convert_line(image, y):
    width, _ = image.size
    line = ""
    current_letter = get_terrain_letter(image.getpixel((0, y)))
    current_count = 1
    for x in range(1, width):
        pixel = image.getpixel((x, y))
        letter = get_terrain_letter(pixel)
        if letter == current_letter:
            current_count += 1
        else:
            line += current_letter
            line += str(current_count)
            current_letter = letter
            current_count = 1
    line += current_letter
    line += str(current_count)
    return line

# Writers
def write_lua_line(output, line):
    output.write('\t"')
    output.write(line)
    output.write('"')

# Actual conversion code
def convert(image, data_name, output):
    _, height = image.size
    lines = []
    for y in tqdm(range(0, height)):
        line = convert_line(image, y)
        lines.append(line)
    
    output.write(f"\n{data_name} = {{\n")
    for line in lines[:-1]:
        write_lua_line(output, line)
        output.write(",\n")
    write_lua_line(output, lines[-1]) #last one without comma
    output.write("\n}\n")

def convert_large():
    print("Converting large... ")
    output = open(output_file_path_partial + "_large.lua", 'w')
    convert(large_image, "map_data_large", output)

def convert_regular():
    print("Converting small... ")
    output = open(output_file_path_partial + "_small.lua", 'w')
    convert(small_image, "map_data_small", output)

convert_large()
convert_regular()
print("Conversion done. Now move the generaped world files to the root folder of the mod to use them.")
