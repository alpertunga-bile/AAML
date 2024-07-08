from re import compile
from math import floor

# odd numbers are required
dataset_kernel_one_length = 5

dataset_compression = "zstd"
dataset_compression_level = 22
dataset_max_row_count = 10_000_000

dataset_folder = "datasets"
images_folder = "images"
videos_folder = "videos"

images_used_images_file = "used_images.txt"


get_dataset_version_regex = compile(r"\d+")


dataset_columns = []


def set_dataset_columns() -> None:
    for index in range(dataset_kernel_one_length**2):
        dataset_columns.append(f"pixel_{index}_r")
        dataset_columns.append(f"pixel_{index}_g")
        dataset_columns.append(f"pixel_{index}_b")
        dataset_columns.append(f"pixel_{index}_a")

    div_by_two = int(floor(dataset_kernel_one_length / 2))
    # multiplied by 4 because RGBA format is used
    middle_pixel_index = (div_by_two * dataset_kernel_one_length + div_by_two) * 4

    dataset_columns[middle_pixel_index + 0] = "middle_r"
    dataset_columns[middle_pixel_index + 1] = "middle_g"
    dataset_columns[middle_pixel_index + 2] = "middle_b"
    dataset_columns[middle_pixel_index + 3] = "middle_a"
