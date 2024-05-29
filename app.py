from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from waitress import serve

app = Flask(__name__)


model = load_model("model.h5")
labels = ("5", "10", "20", "50", "100", "200")



@app.route('/predict', methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    try:
        img = Image.open(file.stream).convert('L')
        img = img.resize((256, 256), Image.Resampling.LANCZOS)
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        prediction = model.predict(img)
        print("helloooo",prediction)
        label = labels[np.argmax(prediction)]
        return jsonify({'para': label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == "__main__":
    serve(app, host="localhost", port=5070)

