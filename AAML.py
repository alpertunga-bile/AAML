from Database import Database
from Texture import Texture
import os
from tqdm import tqdm

class AAML:
    def __init__(self) -> None:
        pass

    def __init__(self, texture_base_path_file, zip_file):
        fileList = os.listdir(texture_base_path_file)
        for file in fileList:
            split = os.path.splitext(file)
            if "png" in split[1] or "jpg" in split[1] or "jpeg" in split[1]:
                self.texture_paths.append(os.path.join(texture_base_path_file, file))

        if len(self.texture_paths) == 0:
            print(f"In {texture_base_path_file}, there are no png files")
            exit(0)

        self.database = Database(zip_file)
        self.texture_base_file = texture_base_path_file
    
    def Save(self):
        self.database.Save()

    def CheckIfTextureUsed(self, usedList, name):
        for used in usedList:
            if name in used:
                return True
        return False

    def WriteToUsedFile(self, name):
        file = open(self.texture_base_file, "used.txt", "a")
        file.writelines(name)
        file.close()
    
    def AddToDataset(self):
        if self.database is None:
            print("Database variable is None")
            return

        print(f"{len(self.texture_paths)} image(s) are found ...")

        file = open(os.path.join(self.texture_base_file, "used.txt"), "r")
        usedTextureNames = file.readlines()
        file.close()

        for texture_path in self.texture_paths:
            if self.CheckIfTextureUsed(usedTextureNames, texture_path) is True:
                print(f"{texture_path} is used for this database | Skipping ...")
                continue

            texture = Texture(texture_path)
            pixelList = []
            
            for y in tqdm(range(1, texture.height - 1), desc=f"{texture_path}"):
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
            self.WriteToUsedFile(texture_path)
            

    texture_base_file = None
    texture_paths = []
    database = None