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
chunk_sizes = [32, 8]
resize_width = 1000 # or None

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

# Debug show the image
image.show()

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



width, height = image.size
chunk = Chunk(image, chunk_sizes, 0, width, 0, height)
output.write("chunk_sizes = %s\n" % chunk_sizes)

jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
pickled = jsonpickle.encode(chunk, unpicklable=False)
output.write(pickled)
