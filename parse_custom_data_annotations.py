import argparse
from yolov6.custom_data import data

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml_annotation_folder", type=str, required=True, help="Path to the folder with the xml annotation files")
    parser.add_argument("--annotation_names_path", type=str, required=True, help="Path to the annotation_classes.txt file")
    parser.add_argument("--save_folder", type=str, required=True, help="Path to the folder where the annotations should be saved as txt files. The txt files have the same name as the image files, with different extension.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    data.load_annotations(args.xml_annotation_folder, args.save_folder, args.annotation_names_path)