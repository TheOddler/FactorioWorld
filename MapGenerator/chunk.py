import math
from helpers import is_water

# Constants
water = 0
ground = 1

class Chunk:
    def __init__(self, image, chunk_sizes, from_x, to_x, from_y, to_y):
        if (from_x > to_x): raise AssertionError("From x must be smaller than to x")
        if (from_y > to_y): raise AssertionError("From y must be smaller than to y")

        self.from_x = from_x
        self.to_x = to_x
        self.from_y = from_y
        self.to_y = to_y
        self.data = None # list of chunks, or a single number (water/ground)

        if (len(chunk_sizes) > 0):
            self.divide_into_chunks(chunk_sizes, image)
        else:
            self.parse_pixels(image)
        
        self.prune_data()

    def divide_into_chunks(self, chunk_sizes, image):
        chunk_size = chunk_sizes[0]
        remaining_chunk_sizes = chunk_sizes[1:]
        chunk_count_x = math.ceil( (self.to_x - self.from_x) / chunk_size )
        chunk_count_y = math.ceil( (self.to_y - self.from_y) / chunk_size )

        self.data = []
        for chunk_y in range(0, chunk_count_y):
            for chunk_x in range(0, chunk_count_x):
                from_x = self.from_x + chunk_x * chunk_size
                from_y = self.from_y + chunk_y * chunk_size

                to_x = self.from_x + (chunk_x + 1) * chunk_size
                to_y = self.from_y + (chunk_y + 1) * chunk_size
                to_x = min(to_x, self.to_x)
                to_y = min(to_y, self.to_y)

                chunk = Chunk(image, remaining_chunk_sizes, from_x, to_x, from_y, to_y)
                self.data.append(chunk)
    
    def parse_pixels(self, image):
        pixels = []
        for y in range(self.from_y, self.to_y):
            for x in range(self.from_x, self.to_x):
                color = image.getpixel((x, y))
                if is_water(color):
                    pixels.append(0)
                else:
                    pixels.append(1)
        self.data = pixels

    def prune_data(self):
        if isinstance(self.data, int):
            return # We are already done
        if isinstance(self.data, list):
            # Check what is in the data, and prune the child chunks
            contains_water = False
            contains_ground = False
            contains_chunks = False
            for d in self.data:
                if d == water:
                    contains_water = True
                elif d == ground:
                    contains_ground = True
                elif isinstance(d, Chunk):
                    d.prune_data()
                    contains_chunks = True
                else:
                    raise AssertionError("Data contains something strange: " + type(d))
            
            if contains_chunks:
                if contains_water or contains_ground:
                    raise AssertionError("Data contains both chunks and numbers, that's not good.")
                cc_water = False
                cc_ground = False
                for chunk in self.data:
                    if chunk.data == water:
                        cc_water = True
                    elif chunk.data == ground:
                        cc_ground = True
                    else:
                        cc_water = True
                        cc_ground = True
                
                if cc_water and cc_ground:
                    pass # Nothing we can prune here
                elif cc_water:
                    self.data = water
                elif cc_ground:
                    self.data = ground
                else:
                    raise AssertionError("Data contains chunks that are nothing?")
            elif contains_water and contains_ground:
                pass # Nothing we can prune here
            elif contains_water:
                self.data = water
            elif contains_ground:
                self.data = ground
            else:
                raise AssertionError("Data contains nothing? What is going on?")
        else:
            raise AssertionError("Data is not an Int, nor a list, wtf is it? " + type(self.data))
