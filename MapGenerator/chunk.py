import math
from helpers import is_water

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

    def _divide(self, chunk_sizes):
        self.chunk_sizes = chunk_sizes

        chunk_size = chunk_sizes[0]
        remaining_chunk_sizes = chunk_sizes[1:]
        
        chunk_count_x = math.ceil( (self.to_x - self.from_x) / chunk_size )
        chunk_count_y = math.ceil( (self.to_y - self.from_y) / chunk_size )

        self.data = []
        for chunk_y in range(0, chunk_count_y):
            for chunk_x in range(0, chunk_count_x):
                _print_progress(chunk_sizes, chunk_count_x * chunk_count_y, chunk_x + chunk_count_x * chunk_y)

                from_x = self.from_x + chunk_x * chunk_size
                from_y = self.from_y + chunk_y * chunk_size

                to_x = self.from_x + (chunk_x + 1) * chunk_size
                to_y = self.from_y + (chunk_y + 1) * chunk_size
                to_x = min(to_x, self.to_x)
                to_y = min(to_y, self.to_y)

                chunk = Chunk(from_x, to_x, from_y, to_y)
                if (remaining_chunk_sizes):
                    chunk._divide(remaining_chunk_sizes)
                self.data.append(chunk)
    
    def _parse(self, image):
        if self.data:
            if not isinstance(self.data, list) or not isinstance(self.data[0], Chunk):
                raise AssertionError("At this point if the chunk has data, it should be a list of chunks")
            self._parse_node(image)
        else:
            self._parse_leaf(image)
        
    def _parse_node(self, image):
        for i, chunk in enumerate(self.data):
            _print_progress(self.chunk_sizes, len(self.data), i)
            chunk._parse(image)

    def _parse_leaf(self, image):
        pixels = []
        for y in range(self.from_y, self.to_y):
            for x in range(self.from_x, self.to_x):
                color = image.getpixel((x, y))
                kind = WATER if is_water(color) else GROUND
                pixels.append(kind)

        self.data = pixels

    def _prune(self):
        if not isinstance(self.data, list):
                raise AssertionError("At this point all data is a list, either full of ints, or full of chunks")

        if isinstance(self.data[0], Chunk):
            contains_water, contains_ground = self._check_data_chunks()
        else:
            contains_water, contains_ground = self._check_data_pixels()
            
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
            raise AssertionError("Data contains nothing?")
    
    def _check_data_chunks(self):
        # Check what is in the data, and prune the child chunks
        contains_water = False
        contains_ground = False
        for i, chunk in enumerate(self.data):
            _print_progress(self.chunk_sizes, len(self.data), i)

            kind = chunk._prune()
            if kind == WATER:
                contains_water = True
            elif kind == GROUND:
                contains_ground = True
            else:
                contains_water = True
                contains_ground = True
        
        return contains_water, contains_ground

    def _check_data_pixels(self):
        contains_water = False
        contains_ground = False
        for kind in self.data:
            if kind == WATER:
                contains_water = True
            elif kind == GROUND:
                contains_ground = True
            else:
                raise AssertionError("Pixel is neither water nor ground... what is going on? " + kind)
        
        return contains_water, contains_ground


    def info(self):
        if isinstance(self.data, list):
            return self.info_list()
        else:
            water = 1 if self.data == WATER else 0
            ground = 1 if self.data == GROUND else 0
            mixed = 0
            nodes = 1
            return water, ground, mixed, nodes

    def info_list(self):
        water_sum = 0
        ground_sum = 0
        mixed_sum = 1 # This one is mixed too
        nodes_sum = 1 # 1 for this node
        if isinstance(self.data[0], Chunk):
            for chunk in self.data:
                water, ground, mixed, nodes = chunk.info()
                water_sum += water
                ground_sum += ground
                mixed_sum += mixed
                nodes_sum += nodes
        return water_sum, ground_sum, mixed_sum, nodes_sum

def convert(image, chunk_sizes):
    width, height = image.size
    chunk = Chunk(0, width, 0, height)

    print("Dividing...", end="")
    chunk._divide(chunk_sizes)
    print()

    print("Parsing...", end="")
    chunk._parse(image)
    print()

    print("Pruning...", end="")
    chunk._prune()
    print()

    return chunk


    
def _print_progress(chunk_sizes, chunk_count, chunk_i):
    chunk_size = str(chunk_sizes[0]).rjust(3)

    percentage = chunk_i / chunk_count
    chunk_count = f"{chunk_count:,}"
    chunk_i = f"{chunk_i + 1:,}".rjust(len(chunk_count))

    info = f"{chunk_i}/{chunk_count} ({percentage:.2%})"
    indent = "\t\t\t\t" * len(chunk_sizes)

    print(f"\r{indent}|{chunk_size}: {info}", end="\r")