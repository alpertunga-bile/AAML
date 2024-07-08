from argparse import ArgumentParser
from os import makedirs
from project_vars import (
    dataset_folder,
    images_folder,
    videos_folder,
    set_dataset_columns,
)

from aaml import AAML

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

    aaml = AAML()
    aaml.start()
