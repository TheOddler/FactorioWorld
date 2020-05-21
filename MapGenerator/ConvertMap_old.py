import os, sys
from PIL import Image
from tqdm import tqdm
from helpers import *

# Settings
image_file = 'NE2_LR_LC_SR_W_DR.tif' #change me for different image
output_file = 'map_compressed.lua' #change me for a different output file
chunk_sizes = [32, 8]
resize_width = None # Number (ex 500) or None

# Globals
Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
image_file = os.path.join(sys.path[0], image_file)
image = Image.open(image_file).convert('RGB') # the image to use

output_file = os.path.join(sys.path[0], output_file)
output = open(output_file, 'w')

# Optionally resize image
if resize_width:
    width, height = image.size
    resize_height = int(float(height)*float(resize_width / float(width)))
    print(f"Resizing image from {width}, {height} to {resize_width}, {resize_height}...")
    image = image.resize((resize_width, resize_height), Image.ANTIALIAS)

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
# def convert_line_custom_compressed(im, y, width):
#     line = ""
#     current_letter = get_terrain_letter(im.getpixel((0, y)))
#     current_count = 1
#     for x in range(1, width):
#         pixel = im.getpixel((x, y))
#         letter = get_terrain_letter(pixel)
#         if letter == current_letter:
#             current_count += 1
#         else:
#             line += current_letter
#             line += str(current_count)
#             current_letter = letter
#             current_count = 1
#     line += current_letter
#     line += str(current_count)
#     return line

def convert_line_land_water(y, width):
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

# Writers
def write_lua_land_water(lines):
    output.write("map_data = {\n")
    for line in lines[:-1]:
        output.write(f"\t{{{ ','.join(str(a) for a in line) }}},\n")
    output.write(f"\t{{{ ','.join(str(a) for a in line) }}}\n") #last one without comma
    output.write("}")

# Actual conversion code
def convert_land_water():
    print("Converting... ")
    print(image.format, image.size, image.mode)
    width, height = image.size
    lines = []
    for y in tqdm(range(0, height)):
        line = convert_line_land_water(y, width)
        lines.append(line)

    write_lua_land_water(lines)
    print("Conversion done.")

convert_land_water()
