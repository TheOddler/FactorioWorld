import os, sys
from PIL import Image
from tqdm import tqdm
from settings import Settings

# Settings
image_file = 'NE2_LR_LC_SR_W_DR.tif' #change me for different image
output_file = 'map_compressed.lua' #change me for a different output file

# Constants
water = 0
ground = 1

# Functions
def color_color_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    #return (r1-r2) ** 2 + (g1-g2) ** 2 + (b1-b2) ** 2
    rm = (r1+r2) / 2
    return ((2+rm) * (r1-r2)) ** 2 + (4 * (g1-g2)) ** 2 + (3-rm * (b1-b2)) ** 2

def is_water(color):
    r, g, b = color
    return b > (r + g) / 2

def in_image(x, y, settings):
    return x < settings.width and y < settings.height

def convert_chunk(x, y, settings):
    found_water = False
    found_ground = False
    chunk_size = settings.chunk_size

    chunk = []
    for pixel_y in range(y * chunk_size, y * chunk_size + chunk_size):
        for pixel_x in range(x * chunk_size, x * chunk_size + chunk_size):
            if in_image(pixel_x, pixel_y, settings):
                if is_water(settings.image.getpixel((pixel_x, pixel_y))):
                    found_water = True
                    chunk.append(water)
                else:
                    found_ground = True
                    chunk.append(ground)
    
    if found_water and found_ground:
        return chunk
    if found_water:
        return water
    if found_ground:
        return ground

def write_lua_chunk(chunk, settings):
    output = settings.output
    if isinstance(chunk, list):
        output.write("\t{")
        for tile in chunk[:-1]:
            output.write("%s" % tile)
            output.write(",")
        output.write("%s" % chunk[-1])
        output.write("}")
    else:
        output.write("\t%s" % chunk)

def write_lua(chunks, settings):
    output = settings.output
    output.write("chunk_size = %s\n" % settings.chunk_size)
    
    output.write("width = %s\n" % settings.width)
    output.write("height = %s\n" % settings.height)

    output.write("map_data = {\n")
    for chunk in tqdm(chunks[:-1]):
        write_lua_chunk(chunk, settings)
        output.write(",\n")
    write_lua_chunk(chunks[-1], settings) #last one without comma
    output.write("}")

def convert(settings):
    chunks = []
    for x in tqdm(range(0, settings.chunk_count_x)):
        for y in range(0, settings.chunk_count_y):
            chunk = convert_chunk(x, y, settings)
            chunks.append(chunk)
    return chunks

def print_info(chunks, settings):
    print("size = %s; " % settings.size)
    print("chunk_size = %s\n" % settings.chunk_size)

    total = len(chunks)
    print("chunks: x = %s, y = %s, total: %s\n" % (settings.chunk_count_x, settings.chunk_count_y, total))

    water_count = 0
    ground_count = 0
    mixed_count = 0
    for chunk in chunks:
        if isinstance(chunk, list):
            mixed_count += 1
        elif chunk == water:
            water_count += 1
        elif chunk == ground:
            ground_count += 1
    
    print("water_count = %s (%.2f%%)\n" % (water_count, water_count / total * 100))
    print("ground_count = %s (%.2f%%)\n" % (ground_count, ground_count / total * 100))
    print("mixed_count = %s (%.2f%%)\n" % (mixed_count, mixed_count / total * 100))
    print("Output size = %s\n" % os.path.getsize(settings.output_file))
    print("\n")
    print("\n")

# # Do the actual converting
# # chunk_size = 4 # 3 636
# # chunk_size = 8 # 2 714; 28 030
# # chunk_size = 16 # 3 728
# # chunk_size = 32 # 5 345
# chunk_s = 64 # 7 299; 75 383
# # chunk_size = 128 # 10243
settings = Settings(image_file, output_file, 16, 4000)
for s in [4, 8, 16, 32, 64, 128]:
    settings.set_output_file(output_file + str(s))
    settings.chunk_size = s
    chunks = convert(settings)
    write_lua(chunks, settings)
