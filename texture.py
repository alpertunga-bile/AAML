from PIL import Image
from os.path import exists, join


class Texture:
    _pixels = None
    width = 0
    height = 0

    def __init__(self, filename: str, images_folder: str) -> None:
        image_path = join(images_folder, filename)

        if exists(image_path) is False:
            print(f"{image_path} is not exists")
            return

        img = Image.open(image_path)

        if img.mode == "RGB":
            img = img.convert("RGBA")

        self._pixels = img.load()
        self.width = img.width
        self.height = img.height

        img.close()

    def get_pixel(self, x: int, y: int) -> tuple[int, int, int, int]:
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return (0, 0, 0, 255)

        try:
            pixel_val = self._pixels[x, y]
        except:
            pass

        return pixel_val
