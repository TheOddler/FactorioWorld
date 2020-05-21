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

def to_lua(thing, indent = 0, last = True):
    string = ""
    if isinstance(thing, list):
        indent1 = indent + 1 if indent is not None else None
        string += newline_indent(indent)
        string += "{"
        string += newline_indent(indent1)

        for sub_thing in thing[:-1]:
            string += to_lua(sub_thing, indent1, False)
        string += to_lua(thing[-1], indent1, True)

        string += newline_indent(indent)
        string += "}"
        if not last:
            string += ","
        string += newline_indent(indent)
    else:
        string = str(thing)
        if not last:
            string += ","
    return string

def newline_indent(indent):
    if indent is not None:
        return "\n" + "\t" * indent
    else:
        return ""
    
def print_dividing_info(chunk_sizes, chunk_count_x, chunk_count_y, chunk_x, chunk_y):
    if chunk_sizes:
        chunk_size = chunk_sizes[0]
    else:
        chunk_size = 1
    chunk_size = str(chunk_size).rjust(3)

    chunk_count_x = str(chunk_count_x)
    chunk_count_y = str(chunk_count_y)
    chunk_x = str(chunk_x + 1).rjust(len(chunk_count_x))
    chunk_y = str(chunk_y + 1).rjust(len(chunk_count_y))

    x_info = f"{chunk_x}/{chunk_count_x}"
    y_info = f"{chunk_y}/{chunk_count_y}"

    indent = "\t\t\t\t" * len(chunk_sizes)

    # print(f"{indent}|{chunk_size}:{x_info}-{y_info}", end="\r", flush=True)
    print(f"\r{indent}|{chunk_size}: {x_info}-{y_info}", end="\r")

def time_s_to_hms(seconds):
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds) 