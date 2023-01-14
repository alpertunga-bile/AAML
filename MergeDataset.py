import pandas as pd
import os
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import gc
from tqdm import tqdm

class MergeDataset:
    def __init__(self, database_path='dataset.zip'):
        self.database_path = database_path
        self.ExtractDatasets()

    def ExtractDatasets(self):
        with ZipFile(self.database_path, 'r', ZIP_DEFLATED, compresslevel=6) as zipObject:
            zipObject.extractall(path=os.getcwd())
        zipObject.close()

    def Merge(self):
        filelist = [s for s in os.listdir() if s.endswith('.pkl')]

        dataframe = pd.read_pickle(filelist[0], compression='gzip')

        for i in tqdm(range(1, len(filelist)), desc='Merging Datasets'):
            tmp_dataframe = pd.read_pickle(filelist[i], compression='gzip')
            dataframe = pd.concat([dataframe, tmp_dataframe], axis=0, ignore_index=True)

            del tmp_dataframe
            gc.collect()

            dataframe.drop_duplicates(inplace=True)
            dataframe.reset_index(drop=True, inplace=True)
            if "Unnamed: 0" in dataframe:
                dataframe.drop("Unnamed: 0", inplace=True, axis=1)
            if "index" in dataframe:
                dataframe.drop("index", inplace=True, axis=1)
            if "level_0" in dataframe:
                dataframe.drop("level_0", inplace=True, axis=1)

        dataframe.to_pickle('dataset.pkl', compression='bz2')

        print("Saving datasets into zip file ...")
        zipObject = ZipFile('dataset.zip', 'w', ZIP_DEFLATED, compresslevel=6)

        filelist = [s for s in os.listdir() if s.endswith('.pkl')]

        for file in filelist:
            zipObject.write(file, compress_type=ZIP_DEFLATED, compresslevel=6)
            os.remove(file)
        zipObject.close()

    database_path = None