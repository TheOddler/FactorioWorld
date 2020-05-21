import math
from helpers import is_water, newline_indent, print_dividing_info

# Constants
WATER = 0
GROUND = 1

class Chunk:
    def __init__(self, from_x, to_x, from_y, to_y):
        if (from_x > to_x): raise AssertionError("From x must be smaller than to x")
        if (from_y > to_y): raise AssertionError("From y must be smaller than to y")

        self.from_x = from_x
        self.to_x = to_x
        self.from_y = from_y
        self.to_y = to_y
        self.data = None # list of chunks, or int

    def divide(self, chunk_sizes):
        if chunk_sizes:
            chunk_size = chunk_sizes[0]
            remaining_chunk_sizes = chunk_sizes[1:]
        else:
            chunk_size = 1
        
        chunk_count_x = math.ceil( (self.to_x - self.from_x) / chunk_size )
        chunk_count_y = math.ceil( (self.to_y - self.from_y) / chunk_size )

        self.data = []
        for chunk_y in range(0, chunk_count_y):
            for chunk_x in range(0, chunk_count_x):
                print_dividing_info(chunk_sizes, chunk_count_x, chunk_count_y, chunk_x, chunk_y)

                from_x = self.from_x + chunk_x * chunk_size
                from_y = self.from_y + chunk_y * chunk_size

                to_x = self.from_x + (chunk_x + 1) * chunk_size
                to_y = self.from_y + (chunk_y + 1) * chunk_size
                to_x = min(to_x, self.to_x)
                to_y = min(to_y, self.to_y)

                chunk = Chunk(from_x, to_x, from_y, to_y)
                if (chunk_sizes):
                    chunk.divide(remaining_chunk_sizes)
                self.data.append(chunk)
    
    def parse(self, image):
        if isinstance(self.data, list):
            self.parse_node(image)
        else:
            self.parse_leaf(image)
        
    def parse_node(self, image):
        for chunk in self.data:
            chunk.parse(image)

    def parse_leaf(self, image):
        if (self.from_x != self.to_x - 1): raise AssertionError("This is not a leaf node? " + str(self.from_x) + " != " + str(self.to_x) + " - 1")
        if (self.from_y != self.to_y - 1): raise AssertionError("This is not a leaf node? " + str(self.from_y) + "!=" + str(self.to_y) + " - 1")

        color = image.getpixel((self.from_x, self.from_y))
        if is_water(color):
            self.data = WATER
        else:
            self.data = GROUND

    def prune(self):
        if isinstance(self.data, list):
            return self.prune_node()
        else:
            return self.prune_leaf()
    
    def prune_node(self):
        # Check what is in the data, and prune the child chunks
        contains_water = False
        contains_ground = False
        for chunk in self.data:
            kind = chunk.prune()
            if kind == WATER:
                contains_water = True
            elif kind == GROUND:
                contains_ground = True
            else:
                contains_water = True
                contains_ground = True
        
        if contains_water and contains_ground:
            # Nothing we can prune here
            return None
        elif contains_water:
            self.data = WATER
            return WATER
        elif contains_ground:
            self.data = GROUND
            return GROUND
        else:
            raise AssertionError("Data contains nothing? What is going on?")

    def prune_leaf(self):
        return self.data
    
    def to_lua(self, indent = 0, last = True):
        if isinstance(self.data, list):
            return self.to_lua_node(indent, last)
        else:
            return self.to_lua_leaf(indent, last)

    def to_lua_node(self, indent, last):
        string = ""
        indent1 = indent + 1 if indent is not None else None

        string += newline_indent(indent)
        string += "{"
        string += newline_indent(indent1)

        for chunk in self.data[:-1]:
            string += chunk.to_lua(indent1, False)
        string += self.data[-1].to_lua(indent1, True)

        string += newline_indent(indent)
        string += "}"
        if not last:
            string += ","
        string += newline_indent(indent)

        return string

    def to_lua_leaf(self, indent, last):
        string = str(self.data)
        if not last:
            string += ","
        return string
    

    def info(self):
        if isinstance(self.data, list):
            return self.info_node()
        else:
            return self.info_leaf()

    def info_node(self):
        water_sum = 0
        ground_sum = 0
        mixed_sum = 1 # This one is mixed too
        nodes_sum = 1 # 1 for this node
        for chunk in self.data:
            water, ground, mixed, nodes = chunk.info()
            water_sum += water
            ground_sum += ground
            mixed_sum += mixed
            nodes_sum += nodes
        return water_sum, ground_sum, mixed_sum, nodes_sum

    def info_leaf(self):
        water = 1 if self.data == WATER else 0
        ground = 1 if self.data == GROUND else 0
        mixed = 0
        nodes = 1
        return water, ground, mixed, nodes