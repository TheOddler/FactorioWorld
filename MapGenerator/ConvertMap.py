import os, sys
from PIL import Image
import math
from helpers import time_s_to_hms, roundb, to_lua
from chunk import Chunk, convert
import time

# Settings
image_file = 'NE2_LR_LC_SR_W_DR.tif' #change me for different image
output_file = 'map_compressed.lua' #change me for a different output file
chunk_sizes = [32, 8]
resize_width = None #1000 # or None

# Globals
Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map
image_file = os.path.join(sys.path[0], image_file)
image = Image.open(image_file).convert('RGB') # the image to use

output_file = os.path.join(sys.path[0], output_file)
output = open(output_file, 'w')

def convert_with(chunk_sizes):
    start = time.time()

    chunk = convert(image, chunk_sizes, resize_width)

    print("Writing...", end="")
    output = open(output_file[:-4] + '---' + '-'.join(str(e) for e in chunk_sizes) + ".lua", 'w')
    output.write("chunk_sizes = %s\n" % chunk_sizes)
    output.write("data = ")
    output.write(to_lua(chunk))
    print()

    end = time.time()

    print(f"Elapsed time: {time_s_to_hms(end - start)}")
    water, ground, mixed, nodes = chunk.info()
    print(f"Water: {water}/{nodes} = {water/nodes*100:.1f}%")
    print(f"Ground: {ground}/{nodes} = {ground/nodes*100:.1f}%")
    print(f"Mixed: {mixed}/{nodes} = {mixed/nodes*100:.1f}%")
    print()

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


