import torch
from torchvision import transforms
from PIL import Image
from ultralytics import YOLO
import numpy as np


def inference():
    model = YOLO('best4.pt')

    results = model.predict(source='lyingdown.jpg', conf=0.80)
    print(results[0].boxes)

    if results[0].boxes.cls.size(dim=0) == 0:
        return "trash"
    elif results[0].boxes.cls[np.argmax(results[0].boxes.conf)] == 0:
        return "can"
    elif results[0].boxes.cls[np.argmax(results[0].boxes.conf)] == 1:
        return "glass"
    else:
        return "plastic"

print(inference())