from PIL import Image
from os.path import exists


class Texture:
    _pixels = None
    _width = 0
    _height = 0

    def __init__(self, filepath: str) -> None:
        if exists(filepath) is False:
            print(f"{filepath} is not exists")
            return

        img = Image.open(filepath)

        if img.mode == "RGB":
            img = img.convert("RGBA")

        self._pixels = img.load()
        self._width = img.width
        self._height = img.height

        img.close()

    def get_pixel(self, x: int, y: int):
        if x > self._width or x < 0 or y > self._height or y < 0:
            return (0, 0, 0, 255)

        return self._pixels[x, y]
