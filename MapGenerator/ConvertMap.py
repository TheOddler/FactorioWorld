import os, sys
from PIL import Image
from tqdm import tqdm

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

#terrain_codes = [
#    #((0,0,0), "_", "out-of-map"), #commented out those I don't want to generate
#    ((220,220,254), "o", "deepwater"), #ocean
#    #((24,39,14), "O", "deepwater-green"),
#    ((246,241,254), "w", "water"),
#    #((30,48,16), "W", "water-green"),
#    ((102,184,47), "g", "grass-1"),
#    ((141,187,59), "m", "grass-3"),
#    ((175,209,69), "G", "grass-2"),
#    ((209,194,61), "d", "dirt-3"),
#    ((184,116,46), "D", "dirt-6"),
#    #((241,237,209), "s", "sand-1"),
#    #((227,203,188), "S", "sand-3")
#]

def color_color_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    #return (r1-r2) ** 2 + (g1-g2) ** 2 + (b1-b2) ** 2
    rm = (r1+r2) / 2
    return ((2+rm) * (r1-r2)) ** 2 + (4 * (g1-g2)) ** 2 + (3-rm * (b1-b2)) ** 2

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

# Writers
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

# Actual conversion code
def convert(name, output_name, line_conversion_method = convert_line_custom_compressed, write_method = write_as_lua_array):
    print("Converting: ", name)
    Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
    im = Image.open(name).convert('RGB') # the image to use
    print(im.format, im.size, im.mode)
    width, height = im.size
    lines = []
    for y in tqdm(range(0, height)):
        line = line_conversion_method(im, y, width)
        lines.append(line)

    write_method(lines, output_name)
    print("Conversion done.")

image_location = os.path.join(sys.path[0], 'NE2_LR_LC_SR_W_DR.tif') #change me for different image
output_location = os.path.join(sys.path[0], 'map_compressed.lua') #change me for a different output file
convert(image_location, output_location)
