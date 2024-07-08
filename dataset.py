from project_vars import (
    dataset_columns,
    dataset_compression,
    dataset_compression_level,
    dataset_folder,
    get_dataset_version_regex,
)
from polars import DataFrame, UInt8, Series, read_parquet
from os import listdir
from os.path import join
from typing import OrderedDict


class Dataset:
    _dataframe: DataFrame = None
    _dataset_name: str = None

    def __init__(self) -> None:
        self._dataframe = self.__create_default_dataset()

        latest_version = self.__get_latest_version()
        self._dataset_name = f"dataset_{latest_version}.parquet"

        self.__read_dataframe()

    def print_info(self) -> None:
        if self._dataframe is None:
            print("Dataset is not exists")
            return

        print(self._dataframe.glimpse())

    def print_head(self, row_count: int = 5) -> None:
        if self._dataframe is None:
            print("Dataset is not exists")
            return

        print(self._dataframe.head(row_count))

    def add_row(self, values: list[UInt8]) -> None:
        temp_dataframe = self.__create_dataframe_from_series(values)

        self._dataframe.vstack(temp_dataframe, in_place=True)

    def add_multiple_rows(self, values: OrderedDict[str, list[UInt8]]) -> None:
        series = []

        for col_name, pixel_values in values.items():
            series.append(Series(name=col_name, values=pixel_values, dtype=UInt8))

        self._dataframe.vstack(DataFrame(series), in_place=True)
        self.__drop_duplicates()

    def save(self) -> None:
        self.__drop_duplicates()

        dataset_path = join(dataset_folder, self._dataset_name)

        self._dataframe.write_parquet(
            file=dataset_path,
            compression=dataset_compression,
            compression_level=dataset_compression_level,
        )

        print(f"{self._dataset_name} is saved to datasets folder")

    def __read_dataframe(self) -> None:
        dataset_path = join(dataset_folder, self._dataset_name)
        self._dataframe = read_parquet(dataset_path)

    def __create_default_dataset(self) -> DataFrame:
        return self.__create_dataframe_from_series(None)

    def __create_dataframe_from_series(self, values: list[UInt8]) -> None:
        series = []

        if values is not None:
            assert len(values) == len(dataset_columns)

        if values is None:
            for col_name in dataset_columns:
                series.append(Series(name=col_name, dtype=UInt8))
        else:
            for col_name, value in zip(dataset_columns, values):
                series.append(Series(name=col_name, values=[value], dtype=UInt8))

        return DataFrame(series)

    def __get_latest_version(self) -> int:
        versions = [0]

        for dataset in listdir(dataset_folder):
            versions.extend(list(map(int, get_dataset_version_regex.findall(dataset))))

        return max(versions)

    def __drop_duplicates(self) -> None:
        self._dataframe = self._dataframe.unique()
