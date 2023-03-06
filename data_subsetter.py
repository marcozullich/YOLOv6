import os
import argparse
import shutil

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True, help="Path to the directory containing the images")
    parser.add_argument("--labels_dir", type=str, required=True, help="Path to the directory containing the labels in YOLO format (.txt files, one per image, one line per object, each line containing the class index, the center coordinates and the width and height of the bounding box)")
    parser.add_argument("--output_dir_data", type=str, required=True, help="Path to the directory where the subset images will be saved")
    parser.add_argument("--output_dir_labels", type=str, required=True, help="Path to the directory where the subset labels will be saved")
    parser.add_argument("--subset_classes", type=int, nargs="+", help="The classes to be selected for the subset. Warning: the class indices will be recreated from 0 to n-1, where n is the number of classes in the subset.")
    parser.add_argument("--include_no_classes", action="store_true", help="If set, images with no classes after subset will be included in the subset with a corresponding empty label file. Cannot be selected along with --leftover_classes_to_other")
    parser.add_argument("--leftover_classes_to_other", action="store_true", help="If set, classes not in the subset will be mapped to a new class 'other' (class index n, where n is the number of classes in the subset). Cannot be selected along with --include_no_classes")
    parser.add_argument("--img_extension", type=str, default="jpg", help="The extension of the images (default: jpg)")
    parser.add_argument("--label_extension", type=str, default="txt", help="The extension of the labels (default: txt)")
    return parser.parse_args()


def main():
    args = parse_args()

    os.makedirs(args.output_dir_data, exist_ok=True)
    os.makedirs(args.output_dir_labels, exist_ok=True)
    num_initial_images = len(os.listdir(args.output_dir_data))
    num_initial_labels = len(os.listdir(args.output_dir_labels))

    if num_initial_images > 0 or num_initial_labels > 0:
        raise RuntimeError(f"Found {num_initial_images} images and {num_initial_labels} labels in the input directories. Please delete them or indicate another two destination folders.")


    # Check that the include_no_classes and leftover_classes_to_other options are not selected together
    if args.include_no_classes and args.leftover_classes_to_other:
        raise ValueError("The --include_no_classes and --leftover_classes_to_other options cannot be selected together")

    # Get the list of images and labels
    images = sorted([os.path.join(args.data_dir, img) for img in os.listdir(args.data_dir) if img.endswith(args.img_extension)])
    labels = sorted([os.path.join(args.labels_dir, label) for label in os.listdir(args.labels_dir) if label.endswith(args.label_extension)])

    # Check the 1:1 correspondence between images and labels
    for img, lab in zip(images, labels):
        if os.path.splitext(img_name := os.path.basename(img))[0] != os.path.splitext(label_name := os.path.basename(lab))[0]:
            raise RuntimeError(f"The images and labels are not the same. Found {img_name} and {label_name}.")

    # Check that the subset classes are valid
    if args.subset_classes is not None:
        for subset_class in args.subset_classes:
            if subset_class < 0:
                raise ValueError("The subset classes must be positive")


    # Create the mapping between the subset classes and the new classes
    subset_classes = sorted(args.subset_classes)
    class_mapping = {}
    for i, subset_class in enumerate(subset_classes):
        class_mapping[subset_class] = i
    if args.leftover_classes_to_other:
        class_mapping["other"] = len(subset_classes)

    # Create the subset
    for image, label in zip(images, labels):
        filename = os.path.splitext(os.path.basename(image))[0]

        # Read the label file
        with open(os.path.join(args.labels_dir, label), "r") as f:
            lines = f.readlines()

        # Produce the new label file - it can be empty if leftover_classes_to_other is not selected
        parsed_lines = [(int(line.split()[0]), line.split()[1:]) for line in lines]
        new_lines = []
        for parsed_line in parsed_lines:
            if (old_class_id := parsed_line[0]) in class_mapping.keys():
                new_lines.append((class_mapping[old_class_id], parsed_line[1]))
            elif args.leftover_classes_to_other:
                new_lines.append((class_mapping["other"], parsed_line[1]))
        
        # Copy the image and save the new label file
        if len(new_lines) > 0 or args.include_no_classes:
            shutil.copy(image, os.path.join(args.output_dir_data, f"{filename}.{args.img_extension}"))

            with open(os.path.join(args.output_dir_labels, f"{filename}.{args.label_extension}"), "w") as f:
                for new_line in new_lines:
                    f.write(f"{new_line[0]} {' '.join(new_line[1])}")


    print(f"Copied {len(os.listdir(args.output_dir_data))} images and {len(os.listdir(args.output_dir_labels))} labels to {args.output_dir_data} and {args.output_dir_labels} respectively.")









if __name__ == "__main__":
    main()