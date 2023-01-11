from AAML import AAML
import argparse
import pandas as pd

def update_dataset(texture_base_file = "textures", deleteImages=False):
    aaml = AAML(texture_base_file, "dataset.zip")
    aaml.AddToDataset(delete=deleteImages)
    aaml.Save()

def start_test():
    aaml = AAML()
    aaml.StartMLTest()
    
def get_info():
    aaml = AAML()
    print(aaml.database.dataframe.info())
    print(aaml.database.dataframe.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete_used", help="Delete the used images based on used.txt in images folder", action='store_true')
    parser.add_argument("--update_dataset", help="Create or update the dataset with given image folder", action='store_true')
    parser.add_argument("--image_file", help="Base image file, default is textures", default="textures", type=str, action='store')
    parser.add_argument("--start_test", help="Start to train and test machine learning models", action='store_true')
    parser.add_argument("--get_info", help="Get dataset info", action='store_true')
    args = parser.parse_args()

    if args.update_dataset:
        update_dataset(args.image_file, args.delete_used)
    elif args.start_test:
        start_test()
    elif args.get_info:
        get_info()