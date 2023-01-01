from AAML import AAML
import argparse
import os

def update_dataset(texture_base_file = "textures", deleteImages=False):
    aaml = AAML(texture_base_file, "dataset.zip")
    aaml.AddToDataset(delete=deleteImages)
    aaml.Save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete_used", help="Delete the used images based on used.txt in images folder", action='store_true')
    parser.add_argument("--update_dataset", help="Create or update the dataset with given image folder", action='store_true')
    parser.add_argument("--image_file", help="Base image file, default is textures", default="textures", type=str, action='store')
    args = parser.parse_args()

    if args.update_dataset:
        update_dataset(args.image_file, args.delete_used)