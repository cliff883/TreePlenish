import os
from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import torch
from matplotlib import pyplot as plt
import numpy as np

app = Flask(__name__)

model = YOLO('best4.pt')

# Mock classification function (replace with your model's inference logic)
def classify_image(image):
    # You should replace this with your actual ML model inference code.
    # Here, we just return a mock result for demonstration purposes.
    image = Image.open(request.files['image'])
    results = model.predict(source=image, conf=0.60)

    print(results[0].boxes)
    # trash
    if results[0].boxes.cls.size(dim=0) == 0:
        return {"trash": 0}
    elif results[0].boxes.cls[np.argmax(results[0].boxes.conf)] == 0:
        return {"can": float(torch.max(results[0].boxes.conf).numpy())}
    elif results[0].boxes.cls[np.argmax(results[0].boxes.conf)] == 2:
        return {"bottle": float(torch.max(results[0].boxes.conf).numpy())}
    else:
        return {"trash": 0}

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected image file'})

    try:
        result = classify_image(image)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # You can change the host and port as needed
