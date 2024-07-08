from dataset import Dataset
from tqdm import tqdm
from gc import collect as gc_collect
from texture import Texture
from os import listdir, remove
from os.path import join, exists
from project_vars import (
    images_folder,
    images_used_images_file,
    dataset_columns,
    dataset_kernel_one_length,
)
from dataset import Dataset
from collections import OrderedDict
from math import floor

images_used_filepath = join(images_folder, images_used_images_file)


class AAML:
    _image_filenames = set()
    _dataset = None

    def __init__(self) -> None:
        for file in listdir(images_folder):
            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".webp")
            ):
                self._image_filenames.add(file)

        if len(self._image_filenames) == 0:
            print(f"There are no image files in the {images_folder} folder")
        else:
            print(f"{len(self._image_filenames)} image(s) are found")

        if exists(images_used_filepath) is False:
            file = open(images_used_filepath, "w")
            file.close()

        self._dataset = Dataset()

    def start(self, delete_used_image_file: bool = False) -> None:
        with open(images_used_filepath, "r") as used_file:
            used_image_names = set([x.strip() for x in used_file.readlines()])

        div_by_two = int(floor(dataset_kernel_one_length / 2))

        for image_filename in tqdm(self._image_filenames, desc="Processed Images"):
            image_filepath = join(images_folder, image_filename)

            if image_filename in used_image_names:
                print(f"{image_filename} is already used")

                if delete_used_image_file:
                    print(f"Deleting {image_filename}")
                    remove(image_filepath)
                continue

            pixel_list = []
            image = Texture(image_filename)

            for y in tqdm(range(0, image.height), desc=f"{image_filename}"):
                for x in range(0, image.width):

                    for height_iter in range(-1 * div_by_two, div_by_two + 1):
                        for width_iter in range(-1 * div_by_two, div_by_two + 1):
                            pixel_list.extend(
                                image.get_pixel(x + width_iter, y + height_iter)
                            )

            self._dataset.add_multiple_rows(
                self.__get_pixel_dict(pixel_list, len(dataset_columns), len(pixel_list))
            )

            del pixel_list
            del image

            self.__write_as_used(image_filename)

            self._dataset.save()

            gc_collect()

    def __get_pixel_dict(
        self, pixel_list: list[int], stride: int, total_count: int
    ) -> OrderedDict[str, list[int]]:
        pixel_dict = OrderedDict()

        for index, col_name in enumerate(dataset_columns):
            pixel_dict[col_name] = []
            current_pos = index

            while current_pos < total_count:
                pixel_dict[col_name].append(pixel_list[current_pos])

                current_pos += stride

        return pixel_dict

    def __write_as_used(self, filename: str) -> None:
        with open(images_used_filepath, "a") as used_file:
            used_file.write(f"{filename}\n")
