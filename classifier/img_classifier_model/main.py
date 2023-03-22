from flask import Flask, request, jsonify, render_template
import os
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('image_classifier.h5')

img_height = 64
img_width = 64
batch_size = 32


def predict_image(image):
    img = image.resize((img_width, img_height))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)
    return predicted_class


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join(
            r'C:/Users/nasru/Documents/CSC2012-Project/classifier/img_classifier_model/uploads/', filename)
        file.save(file_path)
        print(file_path)
        product = 'test'
        print(product)
    else:
        file_path = "not found"
        product = "Unclassified"
    return render_template('predict.html', product=product, user_image=file.filename)


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:

        return jsonify({'error': 'No image provided'}), 400

    image = Image.open(request.files['image']).convert('RGB')

    predicted_class = predict_image(image)
    class_indices = train_generator.class_indices
    classes = {v: k for k, v in class_indices.items()}
    predicted_category = classes[predicted_class]

    response = {
        'Paper': predicted_category == 'Paper',
        'Glass': predicted_category == 'Glass',
        'Plastics': predicted_category == 'Plastics',
        'Metals': predicted_category == 'Metals',
        'Cardboard': predicted_category == 'Cardboard'
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
