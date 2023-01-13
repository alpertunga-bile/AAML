import pandas as pd
import os
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import numpy as np

class Database:
    def __init__(self, database_path):
        if(os.path.exists(database_path) == False or database_path == ""):
            print(f"Cannot found {database_path} file | Creating empty dataset")
            self.dataframe = pd.DataFrame(columns=[
               'top_left_r', 'top_left_g', 'top_left_b', 'top_left_a',
               'top_r', 'top_g', 'top_b', 'top_a',
               'top_right_r', 'top_right_g', 'top_right_b', 'top_right_a',
               'left_r', 'left_g', 'left_b', 'left_a',
               'right_r', 'right_g', 'right_b', 'right_a',
               'bottom_left_r', 'bottom_left_g', 'bottom_left_b', 'bottom_left_a',
               'bottom_r', 'bottom_g', 'bottom_b', 'bottom_a',
               'bottom_right_r', 'bottom_right_g', 'bottom_right_b', 'bottom_right_a',
               'middle_r', 'middle_g', 'middle_b', 'middle_a'   
               ], dtype=np.uint8)
            return

        print("Found zip file | Extracting the dataset")
        with ZipFile(database_path, 'r', ZIP_DEFLATED, compresslevel=6) as zipObject:
            zipObject.extractall(path=os.getcwd())
        zipObject.close()

        for file in os.listdir():
            if ".pkl" in file:
                self.dataset_name = file
            
        self.dataframe = pd.read_pickle(self.dataset_name, compression='gzip')
        if "Unnamed: 0" in self.dataframe:
            self.dataframe.drop("Unnamed: 0", inplace=True, axis=1)
        if "index" in self.dataframe:
            self.dataframe.drop("index", inplace=True, axis=1)

    def SaveToZip(self):
        zipObject = ZipFile('dataset.zip', 'w', ZIP_DEFLATED, compresslevel=6)
        for file in os.listdir():
            if ".pkl" in file:
                zipObject.write(file, compress_type=ZIP_DEFLATED, compresslevel=6)
                os.remove(file)
        zipObject.close()

    def Save(self):
        print("Saving The Dataset ...")
        self.dataframe.to_pickle(self.dataset_name, compression='gzip')
        self.SaveToZip()

    def DropDuplicates(self):
        self.dataframe.drop_duplicates(inplace=True)
        self.dataframe.reset_index(drop=True, inplace=True)

    def AppendRGBA(self, pixelList):
        if(self.dataframe is None):
            return

        if len(pixelList) != 36:
            print("PixelList length is not 36")
            exit(0)
        
        temp_dict = {
            "top_left_r": pixelList[0],
            "top_left_g": pixelList[1],
            "top_left_b": pixelList[2],
            "top_left_a": pixelList[3],
            "top_r": pixelList[4],
            "top_g": pixelList[5],
            "top_b": pixelList[6],
            "top_a": pixelList[7],
            "top_right_r": pixelList[8],
            "top_right_b": pixelList[9],
            "top_right_g": pixelList[10],
            "top_right_a": pixelList[11],
            "left_r": pixelList[12],
            "left_b": pixelList[13],
            "left_g": pixelList[14],
            "left_a": pixelList[15], 
            "right_r": pixelList[16],
            "right_g": pixelList[17],
            "right_b": pixelList[18],
            "right_a": pixelList[19],
            "bottom_left_r": pixelList[20],
            "bottom_left_g": pixelList[21],
            "bottom_left_b": pixelList[22],
            "bottom_left_a": pixelList[23],
            "bottom_r": pixelList[24],
            "bottom_g": pixelList[25],
            "bottom_b": pixelList[26],
            "bottom_a": pixelList[27],
            "bottom_right_r": pixelList[28],
            "bottom_right_g": pixelList[29],
            "bottom_right_b": pixelList[30],
            "bottom_right_a": pixelList[31],
            "middle_r": pixelList[32],
            "middle_g": pixelList[33],
            "middle_b": pixelList[34],
            "middle_a": pixelList[35]
        }

        self.dictionary_list.append(temp_dict)

    def AddToDataset(self):
        print("Adding Pixels To Dataset ...")
        temp_dataframe = pd.DataFrame.from_dict(self.dictionary_list, dtype=np.uint8)
        self.dictionary_list.clear()
        print("Concating Dataframes ...")
        self.dataframe = pd.concat([self.dataframe, temp_dataframe], axis=0, ignore_index=True)
        print("Clearing Duplicates ...")
        self.DropDuplicates()

    dataframe = None
    dataset_name = None
    dictionary_list = []