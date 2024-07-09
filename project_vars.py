from re import compile
from math import floor
from dataclasses import dataclass
from os import makedirs
from torch.cuda import is_available

get_dataset_version_regex = compile(r"\d+")

images_used_images_file = "used_images.txt"

torch_device = "cuda" if is_available() else "cpu"


@dataclass
class DatasetVars:
    # odd numbers are required
    kernel_length = 3

    compression = "zstd"
    compression_level = 22
    max_row_count = 10_000_000

    dataset_folder = "datasets"
    images_folder = "images"
    videos_folder = "videos"

    dataset_columns = []

    def setup(self) -> None:
        makedirs(self.images_folder, exist_ok=True)
        makedirs(self.videos_folder, exist_ok=True)
        makedirs(self.dataset_folder, exist_ok=True)

        self.__set_dataset_columns()

    def __set_dataset_columns(self) -> None:
        for index in range(self.kernel_length**2):
            self.dataset_columns.append(f"pixel_{index}_r")
            self.dataset_columns.append(f"pixel_{index}_g")
            self.dataset_columns.append(f"pixel_{index}_b")
            self.dataset_columns.append(f"pixel_{index}_a")

        div_by_two = int(floor(self.kernel_length / 2))
        # multiplied by 4 because RGBA format is used
        middle_pixel_index = (div_by_two * self.kernel_length + div_by_two) * 4

        self.dataset_columns[middle_pixel_index + 0] = "middle_r"
        self.dataset_columns[middle_pixel_index + 1] = "middle_g"
        self.dataset_columns[middle_pixel_index + 2] = "middle_b"
        self.dataset_columns[middle_pixel_index + 3] = "middle_a"
