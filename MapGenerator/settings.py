import os, sys
from PIL import Image
import math

class Settings:
    def __init__(self, image_file, output_file, chunk_size, resize_width = None, resize_height = None):
        Image.MAX_IMAGE_PIXELS = 1000000000 #large enough to allow huge map

        image_file = os.path.join(sys.path[0], image_file)
        self.image = Image.open(image_file).convert('RGB') # the image to use

        self.set_output_file(output_file)

        self.chunk_size = chunk_size

        if (resize_width is not None):
            self.resize_image(resize_width, resize_height)

    @property
    def size(self):
        return self.image.size

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def chunk_count_x(self):
        return math.ceil(self.width / self.chunk_size)

    @property
    def chunk_count_y(self):
        return math.ceil(self.height / self.chunk_size)

    def resize_image(self, resize_width, resize_height = None):
        if (resize_height is None):
            resize_height = int(float(self.height)*float(resize_width / float(self.width)))
        self.image = self.image.resize((resize_width, resize_height), Image.ANTIALIAS)
    
    def set_output_file(self, output_file):
        output_file = os.path.join(sys.path[0], output_file)
        self.output = open(output_file, 'w')

