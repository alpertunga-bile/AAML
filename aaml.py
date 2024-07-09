from dataset import Dataset
from tqdm import tqdm
from gc import collect as gc_collect
from texture import Texture
from os import listdir, remove
from os.path import join, exists
from project_vars import DatasetVars, images_used_images_file
from dataset import Dataset
from collections import OrderedDict
from math import floor


class AAML:
    _images_used_filepath = None
    _image_filenames = set()
    _dataset = None

    def __init__(self, dataset_vars: DatasetVars) -> None:
        self._images_used_filepath = join(
            dataset_vars.images_folder, images_used_images_file
        )

        for file in listdir(dataset_vars.images_folder):
            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".webp")
            ):
                self._image_filenames.add(file)

        if len(self._image_filenames) == 0:
            print(
                f"There are no image files in the {dataset_vars.images_folder} folder"
            )
        else:
            print(f"{len(self._image_filenames)} image(s) are found")

        if exists(self._images_used_filepath) is False:
            file = open(self._images_used_filepath, "w")
            file.close()

        self._dataset = Dataset(dataset_vars)

    def start(self, delete_used_image_file: bool = False) -> None:
        with open(self._images_used_filepath, "r") as used_file:
            used_image_names = set([x.strip() for x in used_file.readlines()])

        div_by_two = int(floor(self._dataset.dataset_vars.kernel_length / 2))
        total_images = len(self._image_filenames)

        dataset_columns_length = len(self._dataset.dataset_vars.dataset_columns)

        for image_index, image_filename in enumerate(self._image_filenames):
            print(f"Processing images : {image_index + 1} | {total_images}")
            image_filepath = join(
                self._dataset.dataset_vars.images_folder, image_filename
            )

            if image_filename in used_image_names:
                print(f"{image_filename} is already used")

                if delete_used_image_file:
                    print(f"Deleting {image_filename}")
                    remove(image_filepath)
                continue

            image = Texture(image_filename, self._dataset.dataset_vars.images_folder)
            pixel_list = []

            for y in tqdm(range(0, image.height), desc=f"{image_filename}"):

                for x in range(0, image.width):
                    for height_iter in range(div_by_two, (-1 * div_by_two) - 1, -1):
                        for width_iter in range(-1 * div_by_two, div_by_two + 1):
                            pixel_list.extend(
                                image.get_pixel(x + width_iter, y + height_iter)
                            )

            pixel_dict = OrderedDict()
            for col_name in self._dataset.dataset_vars.dataset_columns:
                pixel_dict[col_name] = []

            self.__fill_pixel_dict(
                pixel_dict,
                pixel_list,
                dataset_columns_length,
                len(pixel_list),
            )

            self._dataset.add_multiple_rows(pixel_dict)

            del pixel_dict
            del pixel_list
            del image

            self.__write_as_used(image_filename)

            self._dataset.save()

            gc_collect()

    def __fill_pixel_dict(
        self,
        pixel_dict: OrderedDict[str, list[int]],
        pixel_list: list[int],
        stride: int,
        total_count: int,
    ):
        for index, col_name in enumerate(self._dataset.dataset_vars.dataset_columns):
            current_pos = index

            while current_pos < total_count:
                pixel_dict[col_name].append(pixel_list[current_pos])

                current_pos += stride

    def __write_as_used(self, filename: str) -> None:
        with open(self._images_used_filepath, "a") as used_file:
            used_file.write(f"{filename}\n")
