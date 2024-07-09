from argparse import ArgumentParser
from dataset import Dataset
from torch_dataset import TorchDataset
from aaml import AAML
from project_vars import DatasetVars
from torch_model import TorchModel

from torch.nn import MSELoss
from torch.optim import AdamW
from torch.utils.data import DataLoader

if __name__ == "__main__":
    dataset_vars = DatasetVars()

    parser = ArgumentParser(
        prog="AAML",
        description="Trying to solve the anti aliasing problem with the machine learning algorithms",
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
    parser.add_argument(
        "-i", "--info", action="store_true", help="Get info about the latest dataset"
    )
    parser.add_argument(
        "-e",
        "--enhance",
        action="store_true",
        help="Enhance the dataset",
    )
    parser.add_argument("-t", "--train", action="store_true", help="Train the AI model")
    args = parser.parse_args()

    dataset_vars.kernel_length = int(args.kernel_length)
    dataset_vars.dataset_folder = args.dataset_folder
    dataset_vars.images_folder = args.images_folder
    dataset_vars.videos_folder = args.videos_folder

    dataset_vars.setup()

    if args.info:
        row_count = int(args.row_count)
        dataset = Dataset(dataset_vars)
        print(" Dataset Informations ".center(100, "-"))
        dataset.print_head(row_count)
        dataset.print_info()
        exit(0)

    if args.enhance:
        aaml = AAML(dataset_vars)
        aaml.start(args.delete)

    torch_dataset = TorchDataset("datasets/dataset_0.parquet")

    torch_dataloader = DataLoader(
        dataset=torch_dataset, batch_size=32, num_workers=8, shuffle=True
    )

    model = TorchModel(dataset_vars.kernel_length)
    loss_fn = MSELoss()
    optimizer = AdamW(params=model.parameters(), lr=0.001)

    predict_vals, middle_vals = next(iter(torch_dataloader))

    y = model(predict_vals)

    print(y)

    print(predict_vals.shape)
