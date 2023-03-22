# from flask import Flask, request, jsonify, render_template
# import os
# import numpy as np
# from PIL import Image
# import tensorflow as tf
# import pickle

# app = Flask(__name__)

# # Load the trained model
# model = tf.keras.models.load_model('image_classifier.h5')

# with open('class_indices.pkl', 'rb') as f:
#     class_indices = pickle.load(f)


# img_height = 64
# img_width = 64
# batch_size = 32


# def predict_image(image, class_indices):
#     img = image.resize((img_width, img_height))
#     img_array = np.array(img) / 255.0
#     img_array = np.expand_dims(img_array, axis=0)
#     prediction = model.predict(img_array)
#     predicted_class = np.argmax(prediction)
#     return predicted_class


# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'image' not in request.files:

#         return jsonify({'error': 'No image provided'}), 400

#     image = Image.open(request.files['image']).convert('RGB')

#     predicted_class = predict_image(image, class_indices)
#     class_indices = class_indices.class_indices
#     classes = {v: k for k, v in class_indices.items()}
#     predicted_category = classes[predicted_class]

#     response = {
#         'Paper': predicted_category == 'Paper',
#         'Glass': predicted_category == 'Glass',
#         'Plastics': predicted_category == 'Plastics',
#         'Metals': predicted_category == 'Metals',
#         'Cardboard': predicted_category == 'Cardboard'
#     }

#     return jsonify(response)


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     return render_template('home.html')


# @app.route("/prediction", methods=['GET', 'POST'])
# def prediction():
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = file.filename

#         # slashes should be handeled properly
#         file_path = os.path.join(
#             r'C:/Users/nasru/Document/CSC2012-Project/classifier/img_classifier_model/static/uploads/', filename)
#         file.save(file_path)

#         file_path_image = "/static/uploads/" + filename

#         # run CV command here
#         product = "Classifier"
#         print(product)

#     return render_template('prediction.html', product=product, user_image=file_path_image)


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import pickle
import os
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load the saved model
model = tf.keras.models.load_model('image_classifier.h5')

# Load the saved class indices
with open('class_indices.pkl', 'rb') as f:
    class_indices = pickle.load(f)

# Reverse the class_indices dictionary
classes = {v: k for k, v in class_indices.items()}

img_width = 64
img_height = 64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img = Image.open(file_path).resize((img_width, img_height))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_class = classes[np.argmax(prediction)]

        return jsonify({'class': predicted_class}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
