from AAML import AAML

def create_dataset():
    aaml = AAML("textures", "dataset.zip")
    aaml.AddToDataset()
    aaml.Save()

if __name__ == "__main__":
    create_dataset()