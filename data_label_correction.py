import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Create a subset of the data and labels")
    parser.add_argument("--labels_dir", type=str, required=True, help="The directory containing the labels in txt format")
    parser.add_argument("--correction_type", type=str, default="yolo -> yolov6", choices=["yolo -> yolov6", "yolov6 -> yolo"], help="The type of correction to be applied to the labels. Default: yolo -> yolov6")
    parser.add_argument("--save_folder", type=str, default=None, help="The folder where the corrected labels will be saved. Default: None -> overwrite the original labels")
    return parser.parse_args()

def yolo_to_yolov6(label):
    """Converts a label in YOLO format to YOLOv6 format"""
    label = label.split()
    label[1] = str(float(label[1]) + float(label[3]) / 2)
    label[2] = str(float(label[2]) + float(label[4]) / 2)
    label[3] /= 2
    label[4] /= 2
    return " ".join(label)

def yolov6_to_yolo(label):
    """Converts a label in YOLOv6 format to YOLO format"""
    label = label.split()
    label[1] = str(float(label[1]) - float(label[3]))
    label[2] = str(float(label[2]) - float(label[4]))
    label[3] *= 2
    label[4] *= 2
    return " ".join(label)

def correct_single_label(label_path, correction_type):
    """Corrects a single label line"""
    if correction_type == "yolo -> yolov6":
        return yolo_to_yolov6(label_path)
    elif correction_type == "yolov6 -> yolo":
        return yolov6_to_yolo(label_path)
    raise ValueError(f"Invalid correction type {correction_type}. Allowed values: 'yolo -> yolov6', 'yolov6 -> yolo'")

def correct_label_file(label_path, correction_type, save_folder=None):
    """Corrects a label file. Overwrites the original file if save_folder is None,
    else saves in the specified folder with the same basename."""
    with open(label_path, "r") as f:
        lines = f.readlines()
    corrected_lines = [correct_single_label(label, correction_type) for label in lines]

    save_loc = label_path if save_folder is None else os.path.join(save_folder, os.path.basename(label_path))
    with open(save_loc, "w") as f:
        f.writelines(corrected_lines)

def main():
    args = parse_args()
    for lbl_files in os.listdir(args.labels_dir):
        if lbl_files.endswith(".txt"):
            correct_label_file(os.path.join(args.labels_dir, lbl_files), args.correction_type, args.save_folder)


if __name__ == "__main__":
    main() 