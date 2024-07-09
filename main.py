from argparse import ArgumentParser
from os import makedirs
from project_vars import (
    dataset_folder,
    images_folder,
    videos_folder,
    set_dataset_columns,
)

from dataset import Dataset
from aaml import AAML

if __name__ == "__main__":
    makedirs(images_folder, exist_ok=True)
    makedirs(videos_folder, exist_ok=True)
    makedirs(dataset_folder, exist_ok=True)

    set_dataset_columns()

    parser = ArgumentParser()
    parser.add_argument(
        "--info", action="store_true", help="Get info about the latest dataset"
    )
    parser.add_argument(
        "-rc",
        "--row_count",
        action="store",
        help="Printed row count for the info",
        default=5,
    )
    args = parser.parse_args()

    if args.info:
        row_count = int(args.row_count)
        dataset = Dataset()
        print(" Dataset Informations ".center(100, "-"))
        dataset.print_head(row_count)
        dataset.print_info()
