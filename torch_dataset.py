from torch import Tensor, tensor
from typing import Tuple
from collections import namedtuple
from torch.utils.data.dataset import Dataset as torch_Dataset
from polars import read_parquet

Row = namedtuple("Row", ["predict", "middle"])


class TorchDataset(torch_Dataset):
    _rows: list[Row]

    def __init__(self, dataset_path) -> None:
        super().__init__()

        self._rows = []

        dataset = read_parquet(dataset_path)

        row_dicts = dataset.rows(named=True)

        for row_dict in row_dicts:
            predict_values = []
            middle_values = []

            for col_name, value in row_dict.items():
                if col_name.startswith("middle"):
                    middle_values.append(value / 255.0)
                else:
                    predict_values.append(value / 255.0)

            self._rows.append(Row(predict_values, middle_values))

    def __len__(self) -> int:
        return len(self._rows)

    def __getitem__(self, index: int) -> Tuple[Tensor, Tensor]:
        predict_values = self._rows[index].predict
        middle_values = self._rows[index].middle

        predict_tensor = tensor(predict_values)
        middle_values = tensor(middle_values)

        return (predict_tensor, middle_values)
