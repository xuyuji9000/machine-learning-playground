from flask import Flask, jsonify, request

app = Flask(__name__)

from PIL import Image
import io
import torchvision.transforms as transforms

def transform_image(image_bytes):   
    image = Image.open(io.BytesIO(image_bytes))

    # define custom transform function
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])
    ])

    my_tensor = my_transforms(image)
    my_tensor = my_tensor.unsqueeze(0)

    return my_tensor


# 1. Load densenet model
from torchvision import models

model = models.densenet121(weights='IMAGENET1K_V1')
model.eval()


import json 

def get_prediction(image_bytes):
    
    my_tensor = transform_image(image_bytes)

    # 3. get prediction index
    outputs = model.forward(my_tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    
    # 4. Get the predicted name
    imagenet_class_index = json.load(open('./imagenet_class_index.json'))
    
    return imagenet_class_index[predicted_idx]




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_id': class_id, 'class_name': class_name})
        # return jsonify({'class_id': 'class_id', 'class_name': 'class_name'})
