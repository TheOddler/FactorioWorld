import os, sys
from PIL import Image
from tqdm import tqdm
import math
from helpers import *
import json
import jsonpickle
from chunk import Chunk

# Settings
image_file = 'NE2_LR_LC_SR_W_DR.tif' #change me for different image
output_file = 'map_compressed.lua' #change me for a different output file
chunk_sizes = [16, 8, 4]
resize_width = 500 # or None

# Globals
Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
image_file = os.path.join(sys.path[0], image_file)
image = Image.open(image_file).convert('RGB') # the image to use

output_file = os.path.join(sys.path[0], output_file)
output = open(output_file, 'w')

# Optionally resize image
if (resize_width is not None):
    width, height = image.size
    resize_height = int(float(height)*float(resize_width / float(width)))
    image = image.resize((resize_width, resize_height), Image.ANTIALIAS)

def print_info(chunks):
    total = len(chunks)
    print("chunks: %s\n" % total)

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
    print("\n")
    print("\n")


def convert_with(chunk_sizes):
    print("Converting with: ", chunk_sizes)
    width, height = image.size
    chunk = Chunk(0, width, 0, height)
    print("Dividing...")
    chunk.divide(chunk_sizes)
    print("Parsing...")
    chunk.parse(image)
    print("Pruning...")
    chunk.prune()
    print("Writing...")
    output = open(output_file[:-4] + '---' + '-'.join(str(e) for e in chunk_sizes) + ".lua", 'w')
    output.write("chunk_sizes = %s\n" % chunk_sizes)
    output.write("data = ")
    output.write(chunk.to_lua())

jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
convert_with(chunk_sizes)
convert_with(chunk_sizes[:-1])

# part_1 = [128, 64, 32, 16, 8, 4]
# part_2 = [64, 32, 16, 8, 4]
# part_3 = [32, 16, 8, 4]

# for f in part_1:
#     convert_with([f])
#     for s in part_2:
#         if f > s:
#             convert_with([f, s])
#         for t in part_3:
#             if f > s > t:
#                 convert_with([f, s, t])


