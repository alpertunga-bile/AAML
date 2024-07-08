from AAML import AAML
import argparse
from MergeDataset import MergeDataset
from tqdm import tqdm
from os import makedirs


def update_dataset(texture_base_file="textures", deleteImages=False):
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


def merge():
    merge = MergeDataset()
    merge.Merge()


def split_whole():
    aaml = AAML()
    max_value = 20000000
    print(f"Splitting {aaml.database.dataset_name} ...")
    row_count = aaml.database.dataframe.shape[0]

    if row_count < max_value:
        print("Row count is lower than 10 million rows ...")
        aaml.database.SaveToZip()
        return

    dataset_count = int(row_count / max_value)
    count = 0

    row_bounder = 0
    for i in tqdm(range(0, dataset_count), desc="Splitting"):
        dataset = aaml.database.dataframe.iloc[row_bounder : row_bounder + max_value, :]
        dataset.reset_index(inplace=True)
        dataset.to_pickle("dataset_" + str(i + 1) + ".pkl", compression="gzip")
        count = i + 1
        row_bounder = row_bounder + max_value

    if row_count % max_value != 0:
        print("Last touch ...")
        count = count + 1
        dataset = aaml.database.dataframe.iloc[row_bounder:, :]
        dataset.reset_index(inplace=True)
        dataset.to_pickle("dataset_" + str(count) + ".pkl", compression="gzip")

    aaml.database.SaveToZip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delete_used",
        help="Delete the used images based on used.txt in images folder",
        action="store_true",
    )
    parser.add_argument(
        "--update_dataset",
        help="Create or update the dataset with given image folder",
        action="store_true",
    )
    parser.add_argument(
        "--image_file",
        help="Base image file, default is textures",
        default="textures",
        type=str,
        action="store",
    )
    parser.add_argument(
        "--start_test",
        help="Start to train and test machine learning models",
        action="store_true",
    )
    parser.add_argument("--get_info", help="Get dataset info", action="store_true")
    parser.add_argument(
        "--split_whole", help="Split whole dataset into pieces", action="store_true"
    )
    parser.add_argument("--merge", help="Merge the datasets", action="store_true")
    args = parser.parse_args()

    makedirs("images", exist_ok=True)

    if args.update_dataset:
        update_dataset(args.image_file, args.delete_used)
    elif args.start_test:
        start_test()
    elif args.get_info:
        get_info()
    elif args.split_whole:
        split_whole()
    elif args.merge:
        merge()
