import os
from typing import List, Dict

import lxml
from bs4 import BeautifulSoup


def load_annotation_names(annotation_names_path:str) -> List:
    '''
    Loads the annotation names from the annotation_names.txt file
    '''
    names = {}
    with open(annotation_names_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line != "":
                names[line] = i

    return names

def parse_annotation(file:str, names:Dict):
    '''
    Loads the annotation from a single xml file and parses it to YOLO format.

    Parameters
    ----------
    file : str
        The path to the xml file
    names : Dict
        The dictionary of annotation names loaded via load_annotation_names
    '''
    with open(file, "r") as f:
        xml = f.read()
    xml_data = BeautifulSoup(xml, "lxml")

    filename = os.path.splitext(xml_data.find("filename").text)[0]

    width = int(xml_data.find("width").text)
    height = int(xml_data.find("height").text)

    objects = []

    for obj in xml_data.find_all("object"):
        name = obj.find("name").text.strip()
        class_id = names[name]


        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        dx = xmax - xmin
        dy = ymax - ymin
        objects.append((class_id, xmin/width, ymin/height, dx/width, dy/height))
    
    return filename, objects

def save_annotation(save_path:str, filename:str, objects:List):
    '''
    Saves the annotation to a txt file in the YOLO format  (class_id, x_center, y_center, width, height).
    The file is saved under the save_path folder with the name filename.txt

    Parameters
    ----------
    save_path : str
        The path to the folder where the annotation should be saved
    filename : str
        The name of the image file
    objects : List
        The list of objects in the image obtained via parse_annotation
    '''
    with open(os.path.join(save_path, filename + ".txt"), "w") as f:
        for obj in objects:
            f.write(" ".join([str(x) for x in obj]) + "\n")
    return



def load_annotations(annotations_path:str, save_path:str, class_names_file:str):
    '''
    Loads all the annotations from the annotation folder and parses them to YOLO format.

    Parameters
    ----------
    annotations_path : str
        The path to the annotation folder
    save_path : str
        The path to the folder where the annotations should be saved as txt files. The txt files have the same name as the image files, with different extension.
    class_names_file : str
        The path to the annotation_classes.txt file
    '''
    os.makedirs(save_path, exist_ok=True)

    names = load_annotation_names(class_names_file)
    
    for file in os.listdir(annotations_path):
        file = os.path.join(annotations_path, file)
        if file.endswith("xml"):
            filename, objects = parse_annotation(file, names)
            save_annotation(save_path, filename, objects)
    print(f"Annotations loaded into {save_path}")

    

