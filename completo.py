#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 07:53:08 2024

@author: carlosmeza
"""

# Common
#importamos las librerias que necesitamos
import os 
import keras
import numpy as np 
import cv2
import tensorflow as tf
from IPython.display import clear_output as cls

# Data Loading 
#from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# Data Visualization
import plotly.express as px
import matplotlib.pyplot as plt

# Pre-Trained Models
from tensorflow.keras.applications import ResNet50V2, InceptionV3, Xception, ResNet152V2

# Model
from keras.models import Sequential, load_model
from keras.layers import GlobalAveragePooling2D as GAP, Dense, Dropout

# Callbacks
from keras.callbacks import EarlyStopping, ModelCheckpoint

# aqui agregamos la ruta de donde vamos a leer las imagenes
root_path = '/Users/carlosmeza/Documents/Uninorte/Vision por Computador/Dataset/Front/'

# miramos las clases de billetes que vamos a cargar, ignorando archivos ocultos como .DS_Store
class_names = sorted([name for name in os.listdir(root_path) if not name.startswith('.') and os.path.isdir(os.path.join(root_path, name))])

# Verificar número de clases
n_classes = len(class_names)
print(f"Total number of classes : {n_classes}")

# Calculate class distribution, filtrando archivos que no sean imágenes
class_dis = [len([f for f in os.listdir(os.path.join(root_path, name)) if not f.startswith('.')]) for name in class_names]

# Visualise class distribution (gráfico de pastel)
fig = px.pie(names=class_names, values=class_dis, title="Class Distribution", hole=0.4)
fig.update_layout({'title':{'x':0.5}})
fig.show()

# Bar Plot (gráfico de barras)
fig = px.bar(x=class_names, y=class_dis, color=class_names)
fig.show()


# Calculate class distribution
class_dis = [len(os.listdir(root_path + name)) for name in class_names]

# Visualise class distribution
fig = px.pie(names=class_names, values=class_dis, title="Class Distribution", hole=0.4)
fig.update_layout({'title':{'x':0.5}})
fig.show()

# Bar Plot
fig = px.bar(x=class_names, y=class_dis, color=class_names)
fig.show()


# Initialise generator
train_gen = ImageDataGenerator(rescale=1./255, horizontal_flip=False, rotation_range=10, validation_split=0.3)

# Load data
train_ds = train_gen.flow_from_directory(root_path, class_mode='binary' ,shuffle=True, batch_size=32, subset='training')
valid_ds = train_gen.flow_from_directory(root_path, class_mode='binary' ,shuffle=True, batch_size=32, subset='validation')


def show_images(GRID=[4,4], model=None, size=(20,20), data=train_ds):
    n_rows = GRID[0]
    n_cols = GRID[1]
    n_images = n_cols * n_rows
    
    i = 1
    plt.figure(figsize=size)
    for images, labels in data:
        id = np.random.randint(len(images))
        image, label = images[id], class_names[int(labels[id])]
        
        plt.subplot(n_rows, n_cols, i)
        plt.imshow(image)
        
        if model is None:
            title = f"Class : {label}"
        else:
            pred = class_names[int(np.argmax(model.predict(image[np.newaxis, ...])))]
            title = f"Org : {label}, Pred : {pred}"
        
        plt.title(title)
        plt.axis('off')
        
        i+=1
        if i>=(n_images+1):
            break
        cls()
            
    plt.tight_layout()
    plt.show()


show_images()

# Model Name
name = 'ResNet50V2-Colombia-billetes'

# Pre - Trained Model
base_model = ResNet50V2(include_top=False, input_shape=(256,256,3), weights='imagenet')

# Freeze Weights
base_model.trainable = False

# Model Architecture
model = Sequential([
    base_model,
    GAP(),
    Dense(256, activation='relu', kernel_initializer='he_normal'),
    Dense(n_classes, activation='softmax')
], name=name)

# Callbacks 
cbs = [EarlyStopping(patience=3, restore_best_weights=True), ModelCheckpoint(name+'.keras', save_best_only=True)]

# Compiling Model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(train_ds, validation_data=valid_ds, callbacks=cbs, epochs=10)


plt.figure(figsize=(8, 8))

epochs_range= range(10)

plt.plot( epochs_range, history.history['accuracy'], label="Training Accuracy")

plt.plot(epochs_range, history.history['val_accuracy'], label="Validation Accuracy")

plt.axis(ymin=0.5,ymax=1.2)

plt.grid()

plt.title('Model Accuracy')

plt.ylabel('Accuracy')

plt.xlabel('Epochs')

plt.legend(['train', 'validation'])

plt.show()


# Load Model
model_path = "/Users/carlosmeza/Documents/Uninorte/Vision por Computador/Dataset/Front/ResNet50V2-Colombia-billetes.keras"
model = load_model(model_path)

# Model Summar
model.summary()


show_images(model=model, data=valid_ds)


# specify the root path
root_patht = '/Users/carlosmeza/Documents/Uninorte/Vision por Computador/Dataset/Data/'

# Initialise generator
train_gent = ImageDataGenerator(rescale=1./255, horizontal_flip=False, rotation_range=0, validation_split=0.5)

# Load data
train_dst = train_gent.flow_from_directory(root_patht, class_mode='binary' ,shuffle=True, batch_size=32, subset='training')
valid_dst = train_gent.flow_from_directory(root_patht, class_mode='binary' ,shuffle=True, batch_size=32, subset='validation')



def show_images1(GRID=[1,1], model=None, size=(20,20), data=train_dst):
    n_rows = GRID[0]
    n_cols = GRID[1]
    n_images = n_cols * n_rows
    
    i = 1
    plt.figure(figsize=size)
    for images, labels in data:
        id = np.random.randint(len(images))
        image, label = images[id], class_names[int(labels[id])]
        
        plt.subplot(n_rows, n_cols, i)
        plt.imshow(image)
        
        if model is None:
            title = f"Class : {label}"
        else:
            pred = class_names[int(np.argmax(model.predict(image[np.newaxis, ...])))]
            title = f"Org : {label}, Pred : {pred}"
            print(f"Org : {label}, Pred : {pred}")
        
        plt.title(title)
        plt.axis('off')
        
        i+=1
        if i>=(n_images+1):
            break
        cls()
            
    plt.tight_layout()
    plt.show()


show_images1(model=model, data=train_dst)
show_images1(model=model, data=valid_dst)









