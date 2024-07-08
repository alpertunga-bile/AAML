from argparse import ArgumentParser
from os import makedirs
from dataset import Dataset
from project_vars import (
    dataset_folder,
    images_folder,
    videos_folder,
    set_dataset_columns,
    dataset_columns,
)
from collections import OrderedDict

if __name__ == "__main__":
    makedirs(images_folder, exist_ok=True)
    makedirs(videos_folder, exist_ok=True)
    makedirs(dataset_folder, exist_ok=True)

    set_dataset_columns()

    """
    parser = ArgumentParser()
    parser.add_argument(
        "--info", action="store_true", help="Get info about the latest dataset"
    )
    """

    dataset = Dataset()
    temp_vals = OrderedDict()

    for col_name in dataset_columns:
        temp_vals[col_name] = [x for x in range(5)]

    dataset.add_multiple_rows(temp_vals)

    dataset.print_head()

    dataset.save()
