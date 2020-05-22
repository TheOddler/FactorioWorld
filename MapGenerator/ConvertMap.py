import os, sys
import math
from PIL import Image
from tqdm import tqdm
from helpers import *

# Settings
image_file = 'NE2_LR_LC_SR_W_DR.tif' #change me for different image
output_file = 'map_compressed.lua' #change me for a different output file
chunk_sizes = [32, 8]
resize_width = None # Number (ex 500) or None
colour_width = 1/2 # How much smaller should the colour map be, percentage (ex 0.15) or exact number (ex 500)

# Globals
Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
image_file = os.path.join(sys.path[0], image_file)
print(f"Loading image...")
image = Image.open(image_file).convert('RGB') # the image to use

output_file = os.path.join(sys.path[0], output_file)
output = open(output_file, 'w')

# Optionally resize image
if resize_width:
    width, height = image.size
    resize_height = int(float(height)*float(resize_width / float(width)))
    print(f"Resizing image from {width}, {height} to {resize_width}, {resize_height}...")
    large_image = image.resize((resize_width, resize_height), Image.ANTIALIAS)
else:
    large_image = image

# Make smaller image for the colour map
width, height = image.size
if colour_width < 1:
    colour_width = math.floor((resize_width or width) * colour_width)
colour_height = int(float(height)*float(colour_width / float(width)))
print(f"Creating small image with size {colour_width}, {colour_height}...")
small_image = image.resize((colour_width, colour_height), Image.ANTIALIAS)

# Terrain codes
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
def convert_line_land_water(image, y):
    width, _ = image.size
    line = []
    currently_water = True # start with water always
    current_count = 0
    for x in range(0, width):
        pixel = image.getpixel((x, y))
        next_water = is_water(pixel)
        if currently_water == next_water:
            current_count += 1
        else:
            line.append(current_count)
            currently_water = next_water
            current_count = 1
    if current_count > 0:
        line.append(current_count)
    return line

def convert_line_colour(image, y):
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
def write_lua_list(output, list_):
    output.write(f"\t{{{ ','.join(str(a) for a in list_) }}}")

def write_lua_string(output, string):
    output.write('\t"')
    output.write(string)
    output.write('"')

# Actual conversion code
def convert(image, line_converter, line_writer, data_name):
    _, height = image.size
    lines = []
    for y in tqdm(range(0, height)):
        line = line_converter(image, y)
        lines.append(line)
    
    output.write(f"\n{data_name} = {{\n")
    for line in lines[:-1]:
        line_writer(output, line)
        output.write(",\n")
    line_writer(output, lines[-1]) #last one without comma
    output.write("\n}\n")

def convert_land_water():
    print("Converting land/water... ")
    convert(large_image, convert_line_land_water, write_lua_list, "land_water")

def convert_colours():
    print("Converting colours... ")
    convert(small_image, convert_line_colour, write_lua_string, "terrain_types")

# convert_land_water()
convert_colours()
