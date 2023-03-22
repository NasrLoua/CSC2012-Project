import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

import pandas as pd
import numpy as np
from numpy import linalg

import glob
import os
from PIL import Image

import cv2 

from matplotlib import pyplot as plt
from matplotlib.pyplot import imshow


from string import digits
import pickle

dirImage = './classifier/img_classifier_model/Train'
images_path = os.listdir(dirImage)

filenames = []
filename=[]
l = []
c=np.zeros(5, int)
for i in range(5):
    f=[]
    f+=glob.glob(dirImage+"/"+images_path[i]+"/*"+".jpg")
    l.append(images_path[i])
    c[i]+=len(f)
    filenames += f
#     filenames += glob.glob(dirImage+"/"+images_path[i]+"/*"+".jpg")
    #Create_Label
label=[]
for j in range(5):
    for k in range(c[j]):
        label.append(l[j])
data = pd.DataFrame({'path': filenames, 'class': label})

# def data_processing(data):
#     Metal = []
#     Glass = []
#     Paper = []
# #     ForPredict = []
#     Cardboard = []
#     Plastics = []
    
#     im=[]

#     for i, row in data.iterrows():
#         #convert('L') --> convert image to greyscale
# #         img = Image.open(row['path']).convert('L').resize((64,64))
#         img = Image.open(row['path']).resize((64,64))
#         img = np.array(img)
#         im.append(img)
#         trash = row['class']
#         if trash == 'Metal':
#             Metal.append(img)
#         elif (trash == 'Glass'):
#             Glass.append(img)
#         elif (trash == 'Paper'):
#             Paper.append(img)
# #         elif (trash == 'ForPredict'):
# #             ForPredict.append(img)
#         elif (trash == 'Cardboard'):
#             Cardboard.append(img)
#         elif (trash == 'Plastics'):
#             Plastics.append(img)

#     Metal = np.array(Metal)
#     Glass = np.array(Glass)
#     Paper = np.array(Paper)
# #     ForPredict = np.array(ForPredict)
#     Cardboard = np.array(Cardboard)
#     Plastics = np.array(Plastics)
    
#     all_images = np.concatenate((Metal, Glass, Paper, Cardboard, Plastics)) #, ForPredict
#     return all_images, im

# all_images, im = data_processing(data)
# fig = plt.figure(figsize=(100,100))

# Create the training and validation sets
train_data, val_data = train_test_split(data, test_size=0.2, stratify=data['class'], random_state=42)

# Set up the image data generators
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

# Image dimensions
img_height = 64
img_width = 64
batch_size = 32

# Create data generators
train_generator = train_datagen.flow_from_dataframe(train_data, x_col='path', y_col='class', target_size=(img_height, img_width), batch_size=batch_size, class_mode='categorical')
val_generator = val_datagen.flow_from_dataframe(val_data, x_col='path', y_col='class', target_size=(img_height, img_width), batch_size=batch_size, class_mode='categorical')

def build_model():
    model = tf.keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(5, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model



model = build_model()
model.summary()

epochs = 10
history = model.fit(train_generator, validation_data=val_generator, epochs=epochs)

def predict_image(model, image_path):
    img = Image.open(image_path).resize((img_width, img_height))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    class_indices = train_generator.class_indices
    classes = {v: k for k, v in class_indices.items()}
    predicted_class = classes[np.argmax(prediction)]
    return predicted_class


train_accuracy = history.history['accuracy'][-1]
val_accuracy = history.history['val_accuracy'][-1]

print(f"Training accuracy: {train_accuracy:.2%}")
print(f"Validation accuracy: {val_accuracy:.2%}")


# Test the model on a new image
test_dir = './classifier/img_classifier_model/Test'
test_image_files = [f for f in os.listdir(test_dir) if f.endswith('.jpg')]
for image_file in test_image_files:
    test_image_path = os.path.join(test_dir, image_file)
    predicted_class = predict_image(model, test_image_path)
    print(f"Image: {image_file}, Predicted Class: {predicted_class}")


predicted_class = predict_image(model, test_image_path)
print(f"Predicted class: {predicted_class}")


with open('class_indices.pkl', 'wb') as f:
    pickle.dump(train_generator.class_indices, f)

    
model.save('image_classifier.h5')



