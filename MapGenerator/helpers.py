import math

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

def in_image(x, y, image):
    width, height = image.size
    return x < width and y < height

def chunk_count(chunk_size, img_size):
    width, height = img_size
    count_x = math.ceil(width / chunk_size)
    count_y = math.ceil(height / chunk_size)
    return count_x, count_y

def write_lua(output, thing, indent = 0, last = True):
    indent1 = indent + 1 if indent is not None else None
    if isinstance(thing, list):
        write_newline_indent(output, indent)
        output.write("{")
        write_newline_indent(output, indent1)

        for sub_thing in thing[:-1]:
            write_lua(output, sub_thing, indent1, False)
        write_lua(output, thing[-1], indent1, True)

        write_newline_indent(output, indent)
        output.write("}")
        if not last:
            output.write(",")
        write_newline_indent(output, indent)
    else:
        output.write("%s" % thing)
        if not last:
            output.write(",")

def write_newline_indent(output, indent):
    if indent is not None:
        output.write("\n" + "\t" * indent)











def convert_chunk(x, y, chunk_size):
    found_water = False
    found_ground = False
    chunk = []
    for pixel_y in range(y * chunk_size, y * chunk_size + chunk_size):
        for pixel_x in range(x * chunk_size, x * chunk_size + chunk_size):
            if in_image(pixel_x, pixel_y, image):
                if is_water(image.getpixel((pixel_x, pixel_y))):
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

def convert(chunk_sizes):
    pixels = []
    

    chunk_size = chunk_sizes[0]
    chunk_count_x, chunk_count_y = chunk_count(chunk_size, image.size)

    chunks = []
    for x in tqdm(range(0, chunk_count_x)):
        for y in range(0, chunk_count_y):
            chunk = convert_chunk(x, y, chunk_size)
            chunks.append(chunk)
    
    return chunks