from flask import Flask, request, session, jsonify, send_from_directory, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import pickle
import os
from PIL import Image
import numpy as np
import tensorflow as tf
import database
from database import get_database

dbname = get_database()
collection_profile = dbname ['profile']

from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load the saved model
try:
    model = tf.keras.models.load_model('image_classifier.h5')
except OSError as e:
    print("Error opening file:", e)


# Load the saved model
try:
    with open('class_indices.pkl', 'rb') as f:
        class_indices = pickle.load(f)
except OSError as e:
    print("Error opening file:", e)


# Reverse the class_indices dictionary
classes = {v: k for k, v in class_indices.items()}

img_width = 64
img_height = 64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.secret_key = 'my_secret_key'


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

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        uploads_dir = os.path.join(os.getcwd(), 'static\\uploads')

        # Save image locally
        file_path = os.path.join(r'C:/Users/darkp/Desktop/CSC2012-Project/static/uploads/', filename)
        file.save(file_path)

        file_path_image = "/static/uploads/" + filename
        print(uploads_dir)

        # run CV command here
        img = Image.open(file_path).resize((img_width, img_height))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_class = classes[np.argmax(prediction)]
        product = predicted_class
        print(product)
    return render_template('prediction.html', product = product, user_image = file_path_image)  

# Routes for main UI elements
@app.route("/base")
def index():
    return render_template('base.html')


@app.route("/",methods=['GET','POST'])
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    

@app.route("/profile")
def profile():
    return render_template('profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = database.findOneUser(username)
        
        if user and user['password'] == password:
            session['username'] = username
            print('Session username:', session)
            return redirect(url_for('home'))
        elif user:
            return render_template('login.html', error='Invalid password')
        else:
            return render_template('login.html', error='Invalid username')
    else:
        return render_template('login.html')

    

@app.route('/logout')
def logout():
    session.pop('username', None)
    print('Session username:', session)
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        # validate and add user to the database
        database.addUser(name, username, password)
        # redirect to login page after successful registration
        return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=5001,debug=True)
