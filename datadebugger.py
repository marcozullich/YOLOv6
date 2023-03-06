import torch
from yolov6.data.datasets import TrainValDataset
from yolov6.utils.events import load_yaml

if __name__ == "__main__":
    data_dict = load_yaml("data/coco_trials.yaml")
    data_path = data_dict["val"]
    task = "val"
    dataset = TrainValDataset(
        data_path,
        data_dict=data_dict,
        task=task,
    )