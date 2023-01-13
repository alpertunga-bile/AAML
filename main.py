from AAML import AAML
import argparse
import pandas as pd
from tqdm import tqdm

def update_dataset(texture_base_file = "textures", deleteImages=False):
    aaml = AAML(texture_base_file, "dataset.zip")
    aaml.AddToDataset(delete=deleteImages)
    aaml.Save()

def start_test():
    aaml = AAML()
    aaml.StartMLTest()

    aaml.database.SaveToZip()
    
def get_info():
    aaml = AAML()
    print(aaml.database.dataframe.info())
    print(aaml.database.dataframe.head())

    aaml.database.SaveToZip()

def split():
    aaml = AAML()
    print(f"Splitting {aaml.database.dataset_name} ...")
    row_count = aaml.database.dataframe.shape[0]

    if row_count < 10000000:
        print("Row count is lower than 10 million rows ...")
        aaml.database.SaveToZip()
        return

    next_dataset_index = int(aaml.database.dataset_name.split('_')[1][0]) + 1
    new_dataset_name = 'dataset_' + str(next_dataset_index) + '.pkl'

    first_database = aaml.database.dataframe.iloc[:10000000, :]
    print(f'Creating {new_dataset_name} ...')
    second_database = aaml.database.dataframe.iloc[10000000:, :]
    first_database.reset_index(drop=True, inplace=True)
    second_database.reset_index(drop=True, inplace=True)

    first_database.to_pickle(aaml.database.dataset_name, compression='gzip')
    print(f"Saving {new_dataset_name} ...")
    second_database.to_pickle(new_dataset_name, compression='gzip')

    aaml.database.SaveToZip()

def split_all():
    aaml = AAML()
    print(f"Splitting {aaml.database.dataset_name} ...")
    row_count = aaml.database.dataframe.shape[0]

    if row_count < 10000000:
        print("Row count is lower than 10 million rows ...")
        aaml.database.SaveToZip()
        return

    dataset_count = int(row_count / 10000000)
    count = 0

    row_bounder = 0
    for i in tqdm(range(0, dataset_count), desc="Splitting"):
        dataset = aaml.database.dataframe.iloc[row_bounder:row_bounder+10000000, :]
        dataset.reset_index(inplace=True)
        dataset.to_pickle("dataset_" + str(i + 1) + ".pkl", compression="gzip")
        count = (i + 1)
        row_bounder = row_bounder + 10000000

    if row_count % 10000000 != 0:
        print("Last touch ...")
        count = count + 1
        dataset = aaml.database.dataframe.iloc[row_bounder:, :]
        dataset.reset_index(inplace=True)
        dataset.to_pickle("dataset_" + str(count) + ".pkl", compression="gzip")

    aaml.database.SaveToZip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete_used", help="Delete the used images based on used.txt in images folder", action='store_true')
    parser.add_argument("--update_dataset", help="Create or update the dataset with given image folder", action='store_true')
    parser.add_argument("--image_file", help="Base image file, default is textures", default="textures", type=str, action='store')
    parser.add_argument("--start_test", help="Start to train and test machine learning models", action='store_true')
    parser.add_argument("--get_info", help="Get dataset info", action='store_true')
    parser.add_argument("--split_all", help="Split whole dataset into pieces", action='store_true')
    parser.add_argument("--split", help="Split the last dataset into two dataset", action='store_true')
    args = parser.parse_args()

    if args.update_dataset:
        update_dataset(args.image_file, args.delete_used)
    elif args.start_test:
        start_test()
    elif args.get_info:
        get_info()
    elif args.split_all:
        split_all()
    elif args.split:
        split()