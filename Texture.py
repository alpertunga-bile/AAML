from PIL import Image
import os

class Texture:
    def __init__(self, texture_path):
        if(os.path.exists(texture_path) == False):
            print(f"{texture_path} cannot found")
            exit(0)

        self.image = Image.open(texture_path)

        if self.image.mode == "RGB":
            self.image = self.image.convert("RGBA")

        self.pixels = self.image.load()
        self.width = self.image.width
        self.height = self.image.height
        self.mode = self.image.mode
            

    def __del__(self):
        if(self.image is None):
            return
        self.image.close()

        if(self.pixels is None):
            return

        del self.pixels

    def GetPixel(self, x, y):
        if(x > self.width or y > self.height):
            print("X or Y value exceed the boundary")
            return None

        return self.pixels[x, y]

    def PrintPixels(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                print(self.pixels[j, i])

    image = None
    width = 0
    height = 0
    pixels = None
    mode = "NaN"