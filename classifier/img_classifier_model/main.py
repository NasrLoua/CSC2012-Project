from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
from PIL import Image
import tensorflow as tf
import pickle

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('image_classifier.h5')


with open('class_indices.pkl', 'rb') as f:
    class_indices = pickle.load(f)

    

# with open('train_generator.pkl', 'rb') as f:
#    train_generator = pickle.load(f)

img_height = 64
img_width = 64
batch_size = 32



def predict_image(image, class_indices):
    img = image.resize((img_width, img_height))

# def predict_image_type(image_path, train_generator):
   # img_width, img_height = 64, 64

   # img = Image.open(image_path).resize((img_width, img_height))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    class_indices = train_generator.class_indices
    classes = {v: k for k, v in class_indices.items()}
    predicted_class = classes[np.argmax(prediction)]


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:

        return jsonify({'error': 'No image provided'}), 400

    # image = Image.open(request.files['image']).convert('RGB')

    image_path = 'path/to/your/image.jpg'
    predicted_class = predict_image_type(image_path, train_generator)
    print(f"Predicted class: {predicted_class}")


    predicted_class = predict_image(image, class_indices)
    class_indices = class_indices.class_indices
=======
    # predicted_class = predict_image_type(image, train_generator)
   # class_indices = train_generator.class_indices
   
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
