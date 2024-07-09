from torch import nn, Tensor


class TorchModel(nn.Module):
    def __init__(self, kernel_length: int) -> None:
        super().__init__()

        in_feature = (kernel_length**2) * 4 - 4

        self.layer_stack = nn.Sequential(
            nn.Linear(in_features=in_feature, out_features=512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(in_features=512, out_features=256),
            nn.ReLU(),
            nn.Linear(in_features=256, out_features=128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(in_features=128, out_features=4),
        )

    def forward(self, x: Tensor):
        return self.layer_stack(x)
