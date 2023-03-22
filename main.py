from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import pickle
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        uploads_dir = os.path.join(os.getcwd(), 'static\\uploads')
        file_path = os.path.join(r'C:/Users/darkp/Desktop/CSC2012-Project/classifier/img_classifier_model/static/uploads/', filename)                       #slashes should be handeled properly
        file.save(file_path)
        file_path_image = "/static/uploads/" + filename
        print(uploads_dir)

        # run CV command here
        product = "Fine"
        print(product)
    return render_template('predict.html', product = product, user_image = file_path_image)  

if __name__ == '__main__':
    app.run(port=5001, debug=True)
