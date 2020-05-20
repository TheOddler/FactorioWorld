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
        found_water = False
        found_ground = False
        for y in range(self.from_y, self.to_y):
            for x in range(self.from_x, self.to_x):
                color = image.getpixel((x, y))
                # print(x, y, color)
                if is_water(color):
                    pixels.append(0)
                    found_water = True
                else:
                    pixels.append(1)
                    found_ground = True
        
        if found_water and found_ground:
            print("Both")
            self.data = pixels
        elif found_water:
            # print("Water")
            self.data = water
        elif found_ground:
            print("Ground")
            self.data = ground
        else:
            raise AssertionError("Somehow didn't find water nor ground...")

    def prune_data(self):
        if (isinstance(self.data, int)):
            return # We are already done
        if (isinstance(self.data, list)):
            # First prune all children
            for d in self.data:
                if (isinstance(d, int)):
                    return # We are already done
                else:
                    d.prune_data()
            # print(type(self.data))
        else:
            raise AssertionError("Data is not an Int, nor a list, wtf is it? " + type(self.data))
