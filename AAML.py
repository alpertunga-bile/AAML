from Database import Database
from Texture import Texture
import os
from tqdm import tqdm
from statistics import mean

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from tabulate import tabulate

class AAML:
    def __init__(self, texture_base_path_file = "", zip_file = ""):
        if texture_base_path_file == "":
            self.database = Database('dataset.zip')
            return

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

    # TEST Functions

    def CalculateError(self, y_test, predictions):
        temp_list = None
        error_list = []
        for index in range(0, y_test.shape[0]):
            temp_list = y_test.iloc[index].values.flatten().tolist()
            r_error = (predictions[index][0] - temp_list[0]) / (temp_list[0] + 1)
            g_error = (predictions[index][1] - temp_list[1]) / (temp_list[1] + 1)
            b_error = (predictions[index][2] - temp_list[2]) / (temp_list[2] + 1)
            a_error = (predictions[index][3] - temp_list[3]) / (temp_list[3] + 1)
            total_error = (r_error + g_error + b_error + a_error) / 4.0
            error_list.append(total_error)

        return mean(error_list)

    def DoTest(self, model, X, Y):
        mask = np.random.rand(len(X)) <= 0.8
        x_train = X[mask]
        x_test = X[~mask]
        y_train = Y[mask]
        y_test = Y[~mask]

        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        image_error = self.CalculateError(y_test, predictions)

        return image_error

    def StartMLTest(self):
        Y = self.database.dataframe.iloc[:, 32:36]
        X = self.database.dataframe.iloc[:, 0:32]

        scores = []
        scores.append(["Linear Regression", self.DoTest(LinearRegression(), X, Y)])

        print("#######################################################\nTest Results\n#######################################################")
        print(tabulate(scores, headers=["Tests", "Errors"]))

    # Update Dataset Functions

    def Save(self):
        self.database.Save()

    def CheckIfTextureUsed(self, usedList, name):
        for used in usedList:
            if name in used:
                return True
        return False

    def WriteToUsedFile(self, name):
        file = open(os.path.join(self.texture_base_file, "used.txt"), "a")
        file.writelines(name + '\n')
        file.close()
    
    def AddToDataset(self, delete=False):
        if self.database is None:
            print("Database variable is None")
            return

        print(f"{len(self.texture_paths)} image(s) are found ...")

        if(os.path.exists(os.path.join(self.texture_base_file, "used.txt")) is False):
            file = open(os.path.join(self.texture_base_file, "used.txt"), "w")
            file.close()

        file = open(os.path.join(self.texture_base_file, "used.txt"), "r")
        usedTextureNames = file.readlines()
        file.close()
        count = 1

        for texture_path in self.texture_paths:
            print(f"{count} / {len(self.texture_paths)} In Progress ...")
            count = count + 1
            
            if self.CheckIfTextureUsed(usedTextureNames, texture_path) is True:
                print(f"{texture_path} is used for this database | Skipping ...")
                if delete:
                    print(f"Deleting {texture_path}...")
                    os.remove(texture_path)
                continue

            texture = Texture(texture_path)
            pixelList = []
            
            for y in tqdm(range(1, texture.height - 1), desc=f"{texture_path}"):
                for x in range(1, texture.width - 1):
                    pixelList.extend(texture.pixels[x - 1, y - 1]) # top left
                    pixelList.extend(texture.pixels[x    , y - 1]) # top 
                    pixelList.extend(texture.pixels[x + 1, y - 1]) # top right 
                    pixelList.extend(texture.pixels[x - 1, y])     # left
                    pixelList.extend(texture.pixels[x + 1, y])     # right
                    pixelList.extend(texture.pixels[x - 1, y + 1]) # bottom left
                    pixelList.extend(texture.pixels[x    , y + 1]) # bottom 
                    pixelList.extend(texture.pixels[x + 1, y + 1]) # bottom right
                    pixelList.extend(texture.pixels[x    , y])     # middle

                    self.database.AppendRGBA(pixelList)
                    pixelList.clear()

            self.database.AddToDataset()
            print("DONE!!!")
            self.WriteToUsedFile(texture_path)

    texture_base_file = None
    texture_paths = []
    database = None