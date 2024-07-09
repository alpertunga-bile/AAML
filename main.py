from argparse import ArgumentParser
from dataset import Dataset
from aaml import AAML
from project_vars import DatasetVars

if __name__ == "__main__":
    dataset_vars = DatasetVars()

    parser = ArgumentParser(
        prog="AAML",
        description="Trying to solve the anti aliasing problem with the machine learning algorithms",
    )
    parser.add_argument(
        "-i", "--info", action="store_true", help="Get info about the latest dataset"
    )
    parser.add_argument(
        "-rc",
        "--row_count",
        action="store",
        help="Printed row count for the info",
        default=5,
    )
    parser.add_argument(
        "--kernel_length",
        action="store",
        help="Kernel width or height of the squared kernel",
        default=dataset_vars.kernel_length,
    )
    parser.add_argument(
        "-df",
        "--dataset_folder",
        action="store",
        help="Dataset folder to locate and save datasets",
        default=dataset_vars.dataset_folder,
    )
    parser.add_argument(
        "-if",
        "--images_folder",
        action="store",
        help="Image folder to locate the images",
        default=dataset_vars.images_folder,
    )
    parser.add_argument(
        "-vf",
        "--videos_folder",
        action="store",
        help="Video folder to locate the videos",
        default=dataset_vars.videos_folder,
    )
    parser.add_argument(
        "-del",
        "--delete",
        action="store_true",
        help="Delete the used images from the images folder",
        default=False,
    )
    args = parser.parse_args()

    dataset_vars.kernel_length = int(args.kernel_length)
    dataset_vars.dataset_folder = args.dataset_folder
    dataset_vars.images_folder = args.images_folder
    dataset_vars.videos_folder = args.videos_folder

    dataset_vars.setup()

    if args.info:
        row_count = int(args.row_count)
        dataset = Dataset()
        print(" Dataset Informations ".center(100, "-"))
        dataset.print_head(row_count)
        dataset.print_info()

    aaml = AAML(dataset_vars)
    aaml.start(args.delete)
