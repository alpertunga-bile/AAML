dataset_compression = "zstd"
dataset_compression_level = 15

dataset_folder = "datasets"
images_folder = "images"
videos_folder = "videos"

from re import compile

get_dataset_version_regex = compile(r"\d+")

wanted_directions = [
    "top_left",
    "top",
    "top_right",
    "left",
    "right",
    "bottom_left",
    "bottom",
    "bottom_right",
    "middle",
]

dataset_columns = []


def set_dataset_columns() -> None:
    for direction in wanted_directions:
        dataset_columns.append(f"{direction}_r")
        dataset_columns.append(f"{direction}_g")
        dataset_columns.append(f"{direction}_b")
        dataset_columns.append(f"{direction}_a")
