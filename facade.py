"""
Interface script to a subsystem of I/O operations
Facade defines a higher-level interface that makes our subsystem easier
to use.
"""
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report
from time import gmtime, strftime
import pandas as pd





INPUTPATH = 'images/movie_pics/elysium019.jpg'
FIX_IMG_SQR_SIZE = 64

def img_in(filename):
    """read one image from filename and retun image as numpy array"""
    temp_img = Image.open(filename)
    img = np.array(temp_img)
    name = filename.split('.')[-2]
    return name, img

def img_preprocess(img):
    """cuts numpy array (image) into squares of 64x64 (FIX_IMG_SQR_SIZE) incl. 3 colour channels"""
    img_out = []
    x_size = img.shape[0]
    assert x_size > FIX_IMG_SQR_SIZE
    y_size = img.shape[1]
    assert y_size > FIX_IMG_SQR_SIZE
    for x in range(0, x_size, FIX_IMG_SQR_SIZE):
        xstart = x
        xend = xstart+FIX_IMG_SQR_SIZE
        if xend > x_size:
            xstart = x_size-FIX_IMG_SQR_SIZE
            xend = x_size
        for y in range(0, y_size, FIX_IMG_SQR_SIZE):
            ystart = y
            yend = ystart+FIX_IMG_SQR_SIZE
            if yend > y_size:
                ystart = y_size-FIX_IMG_SQR_SIZE
                yend = y_size
            square = img[xstart:xend, ystart:yend,:]
            sq_info = {'sq': square, 'x': xstart, 'y': ystart}
            img_out.append(sq_info)
    return img_out

def load_model():
    # Model reconstruction from JSON file
    with open('keras_cnn/model/model_strides_11-24-50.json', 'r') as f: 
        model = model_from_json(f.read())
    # Load weights into the new model
    model.load_weights('keras_cnn/model/cnn-model_strides_11-24-50.h5')
    return model


def process():
    name, img = img_in(INPUTPATH)
    var = img_preprocess(img)
    # optional: save squares
    #Image.fromarray(square).convert("RGB").save(location_squares+label+"_"+str(x)+"_"+str(y)+".png")
    
    for sq_info in var:
        predict = predict_hot_pxl(sq_info['sq'])
        sq_info['predict'] = predict
        # dict element sq is now obsolete, remove it
        del sq_info['sq']
    # report name, hot_pxl_list

def predict_hot_pxl(square):

    return 0

# LOCATION = 'images/'
# location_src = LOCATION + 'movie_pics/'
# location_squares = LOCATION + 'squares/'
# location_squares_error = LOCATION + 'error_squares/'
# #images = os.listdir(location_src)
# n_images = len(images)
# print(f"[INFO] loading {n_images} images from {location_src}...")
# data = []
# labels = []
# b = 0

# # slice images into FIX_IMG_SQR_SIZExFIX_IMG_SQR_SIZE squares
# # TO DO: fix row selection is not working!
# for image in images:
#     label = image.split('.')[-2]
#     print(label)
#     labels.append(label)


#     img = Image.open(location_squares+'zachariah047_0_192.png')
#     img = np.array(img)
#     plt.imshow(img)















if __name__ == "__main__":
    process()
