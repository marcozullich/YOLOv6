import argparse
import os
import numpy as np
import shutil
import PIL

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--labels_dir", type=str, required=True)
    parser.add_argument("--image_size", type=int, default=None, help="If None -> leave unchanged.")
    parser.add_argument("--save_dir_train", type=str, required=True)
    parser.add_argument("--save_dir_val", type=str, required=True)
    parser.add_argument("--save_dir_train_label", type=str, required=True)
    parser.add_argument("--save_dir_val_label", type=str, required=True)
    parser.add_argument("--data_extension", type=str, default=".jpg")
    parser.add_argument("--labels_extension", type=str, default=".txt")
    parser.add_argument("--pct_train", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=1111)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    images = sorted([os.path.join(args.data_dir, img) for img in os.listdir(args.data_dir) if img.endswith(args.data_extension)])

    if args.image_size is not None:
        print(f"Resizing images to {args.image_size}x{args.image_size}")
        for img in images:
            img_pil = PIL.Image.open(img)
            img_pil = img_pil.resize((args.image_size, args.image_size))
            img_pil.save(img)
        print(f"Resized images to {args.image_size}x{args.image_size}")

    labels = sorted([os.path.join(args.labels_dir, lbl) for lbl in os.listdir(args.labels_dir) if lbl.endswith(args.labels_extension)])
    imgnames = sorted([os.path.splitext(os.path.basename(img))[0] for img in images])

    print(f"Found {len(images)} images and {len(labels)} labels in {args.data_dir} and {args.labels_dir} respectively")
    
    # Check that the image and label file names match
    for imgn, lbl in zip(imgnames, labels):
        assert imgn == (lbln := os.path.splitext(os.path.basename(lbl))[0]), f"Image and label file names do not match ({imgn} != {lbln})"
    print(f"Image and label file names match")
    
    # train-val split
    np.random.seed(args.seed)
    n_train = int(len(images) * args.pct_train)

    seq_permute = np.random.permutation(list(range(len(images))))
    train_idx = seq_permute[:n_train]
    val_idx = seq_permute[n_train:]

    train_images = [images[i] for i in train_idx]
    train_labels = [labels[i] for i in train_idx]
    val_images = [images[i] for i in val_idx]
    val_labels = [labels[i] for i in val_idx]

    # save train
    os.makedirs(args.save_dir_train, exist_ok=True)
    os.makedirs(args.save_dir_train_label, exist_ok=True)
    for img, lbl in zip(train_images, train_labels):
        shutil.copy(img, args.save_dir_train)
        shutil.copy(lbl, args.save_dir_train_label)
    
    print(f"Copied {len(train_images)} training images and labels to {args.save_dir_train}")

    # save val
    os.makedirs(args.save_dir_val, exist_ok=True)
    os.makedirs(args.save_dir_val_label, exist_ok=True)
    for img, lbl in zip(val_images, val_labels):
        shutil.copy(img, args.save_dir_val)
        shutil.copy(lbl, args.save_dir_val_label)
    
    print(f"Copied {len(val_images)} validation images and labels to {args.save_dir_val}")


