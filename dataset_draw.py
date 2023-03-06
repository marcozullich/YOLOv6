import cv2
import argparse
import os

from typing import Dict, List


def load_annotation_names(annotation_names_path:str):
    '''
    Loads the annotation names from the annotation_names.txt file
    '''
    names = []
    with open(annotation_names_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line != "":
                names.append(line)

    return names

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', required=True)
    parser.add_argument('--label_dir', required=True)
    parser.add_argument('--img_ids', nargs="+", type=int, required=True)
    parser.add_argument('--class_names', type=str, required=True, help="Path to annotations_classes.txt file")
    parser.add_argument('--save_dir', type=str, default=None, help="Path to the folder where the annotated images are to be saved. If None, images are shown instead.")
    args = parser.parse_args()
    return args

def load_labels(label_path:str, class_names:Dict):
    labels = []
    with open(label_path, 'r') as f:
        for line in f:
            label = line.split()
            class_name = class_names[int(label[0])]
            x, y, w, h = [float(x) for x in label[1:]]
            labels.append((class_name, x, y, w, h))
    return labels

def draw_labels(img_dict:Dict):
    img = img_dict["img"].copy()
    labels = img_dict["labels"]
    for label in labels:
        class_name, x, y, w, h = label
        x1 = int(x * img.shape[1])
        y1 = int(y * img.shape[0])
        x2 = int((x+w) * img.shape[1])
        y2 = int((y+h) * img.shape[0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, class_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return img

def main():
    args = parse_args()

    if args.save_dir is not None:
        os.makedirs(args.save_dir, exist_ok=True)

    class_names = load_annotation_names(args.class_names)

    formatted_img_ids = []
    for img_id in args.img_ids:
        formatted_img_ids.append(f"{img_id:06d}")
    
    imgs = []
    for img_id in formatted_img_ids:
        img_dict = {}
        img_dict["id"] = img_id
        img_dict["img"] = cv2.imread(os.path.join(args.img_dir, "img" + img_id + ".jpg"))
        img_dict["labels"] = load_labels(os.path.join(args.label_dir, "img" + img_id + ".txt"), class_names)
        imgs.append(img_dict)
    
    for img_dict in imgs:
        img = draw_labels(img_dict)
        if args.save_dir is not None:
            cv2.imwrite(os.path.join(args.save_dir, img_dict["id"] + ".jpg"), img)
        else:
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()