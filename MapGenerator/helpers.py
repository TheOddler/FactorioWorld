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

def roundb(x, base):
    return base * round(x/base)

def write_newline_indent(output, indent):
    if indent is not None:
        return output.write("\n" + "\t" * indent)

def time_s_to_hms(seconds):
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds) 