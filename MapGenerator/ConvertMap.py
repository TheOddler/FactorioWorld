import os, sys
from PIL import Image

# Terrain codes
out_of_map = "_"
deepwater = "o" #ocean
deepwater_green = "O"
water = "w"
water_green = "W"
grass = "g"
grass_medium = "m"
grass_dry = "G"
dirt = "d"
dirt_dark = "D"
sand = "s"
sand_dark = "S"

def get_terrain_letter(pixel):
    r, g, b = pixel
    if r == max(r, g, b):
        return "d"
    if g == max(r, g, b):
        return "g"
    if b == max(r, g, b):
        return "o"

# Convert image to text for lua
def convert_line_full_text(im, y, width):
    line = ""
    for x in range(0, width):
        pixel = im.getpixel((x, y))
        code = get_terrain_letter(pixel)
        line += code
    return line

def convert_line_custom_compressed(im, y, width):
    line = ""
    current_letter = get_terrain_letter(im.getpixel((0, y)))
    current_count = 1
    for x in range(1, width):
        pixel = im.getpixel((x, y))
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

def convert_line_compressed(im, y, width):
    line = convert_line_full_text(im, y, width)
    
    return line

def write_as_txt(lines, output_name):
    output = open(output_name, 'w')
    for line in lines:
        output.write("%s\n" % line)

def write_as_lua_array(lines, output_name):
    output = open(output_name, 'w')
    output.write("map_data = {\n")
    for line in lines[:-1]:
        output.write("\t\"%s\",\n" % line)
    output.write("\t\"%s\"\n" % lines[-1]) #last one without comma
    output.write("}")

def convert(name, output_name, line_conversion_method = convert_line_custom_compressed, write_method = write_as_lua_array):
    print("Converting: ", name)
    Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
    im = Image.open(name).convert('RGB') # the image to use
    print(im.format, im.size, im.mode)
    width, height = im.size
    lines = []
    for y in range(0, height):
        if y % (height / 100) == 0:
            print("... ", int(y * 100 / height), "%")
        line = line_conversion_method(im, y, width)
        lines.append(line)

    write_method(lines, output_name)
    print("Conversion done.")

convert("NE2_LR_LC_SR_W_DR_50.tif", "map_50_compressed.lua")


