from Database import Database
from Texture import Texture
import os

def AddListFromTupleRGBA(tuple):
    _list = []
    _list.append(tuple[0])
    _list.append(tuple[1])
    _list.append(tuple[2])
    _list.append(tuple[3])
    return _list

class AAML:
    def __init__(self) -> None:
        pass

    def __init__(self, texture_base_path_file, zip_file):
        fileList = os.listdir(texture_base_path_file)
        for file in fileList:
            split = os.path.splitext(file)
            if "png" in split[1]:
                self.texture_paths.append(os.path.join(texture_base_path_file, file))

        if len(self.texture_paths) == 0:
            print(f"In {texture_base_path_file}, there are no png files")
            exit(0)

        self.database = Database(zip_file)
    
    def Save(self):
        self.database.Save()
    
    def AddToDataset(self):
        if self.database is None:
            print("Database variable is None")
            return

        print(f"{len(self.texture_paths)} PNG image(s) found ...")

        for texture_path in self.texture_paths:
            print(f"{texture_path} is processing ...")
            texture = Texture(texture_path)
            pixelList = []
            
            for y in range(1, texture.height - 1):
                for x in range(1, texture.width - 1):
                    pixelList.extend(texture.GetPixel(x - 1, y - 1))
                    pixelList.extend(texture.GetPixel(x, y - 1))
                    pixelList.extend(texture.GetPixel(x - 1, y - 1))
                    pixelList.extend(texture.GetPixel(x, y - 1))
                    pixelList.extend(texture.GetPixel(x + 1, y - 1))
                    pixelList.extend(texture.GetPixel(x - 1, y))
                    pixelList.extend(texture.GetPixel(x + 1, y))
                    pixelList.extend(texture.GetPixel(x + 1, y + 1))
                    pixelList.extend(texture.GetPixel(x, y + 1))
                    pixelList.extend(texture.GetPixel(x + 1, y + 1))
                    pixelList.extend(texture.GetPixel(x, y))
                    
                    self.database.AppendRGBA(pixelList)
                    pixelList.clear()

            self.database.DropDuplicates()
            print("DONE!!!")

    texture_paths = []
    database = None