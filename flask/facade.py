"""
Interface script to a subsystem of I/O operations
Facade defines a higher-level interface that makes te Error Classifier easier
to use.
"""
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
from keras.models import model_from_json
from sklearn.metrics import classification_report
from time import gmtime, strftime
import pandas as pd
import collections
import logging

INPUTPATH = '/home/pepper/Projects/spiced/final_project/images/movie_pics/elysium019.jpg'
FIX_IMG_SQR_SIZE = 64
SQ_OUT = collections.namedtuple('SQ_OUT',['sq', 'x', 'y', 'pred_float', 'pred_int'])
THRESHOLD = 0.5

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
datefmt='%m/%d/%Y %H:%M:%S',
filename='example.log',
filemode='w',
level=logging.WARNING)

def video_in(filename):
    logging.error(filename)
    return filename

def img_in(filename):
    """read one colour image from filename,
    return image as numpy array"""
    temp_img = Image.open(filename)
    img = np.array(temp_img)
    name = filename.split('.')[-2]
    return name, img

def img_preprocess(img):
    """cut numpy array (colour image) into squares of 64x64 (FIX_IMG_SQR_SIZE),
    return squares with associated, x and y coordinates in a dictionary."""
    squares = []
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
            squares.append(SQ_OUT(square, xstart, ystart, 0.0, 0))
    return squares

def load_model():
    # Model reconstruction from JSON file
    with open('/home/pepper/Projects/spiced/final_project/keras_cnn/model/model_strides_11-24-50.json', 'r') as f:
        model = model_from_json(f.read())
    # Load weights into the new model
    model.load_weights('/home/pepper/Projects/spiced/final_project/keras_cnn/model/cnn-model_strides_11-24-50.h5')
    return model

def predict_hot_pxl(sqr, model):
    """takes a numpy array (colour image) size 64x64 and a ML model,
    returnes float number between 0 - 1 for hot pixel detection,
    for 0 no hot pixel detected, 1 hot pixel detected"""
    predict = model.predict(sqr.reshape(1,64,64,3))
    y_pred = [i[0] for i in predict]
    return y_pred

def process():
    #THRESHOLD = 0.5
    model = load_model()
    name, img = img_in(INPUTPATH)
    squares_dict = img_preprocess(img)
    print(squares_dict[0].x)
    # optional: save squares
    #Image.fromarray(square).convert("RGB").save(location_squares+label+"_"+str(x)+"_"+str(y)+".png")
    for sq in squares_dict:
        print(sq.x)
        predict = predict_hot_pxl(sq.sq, model)
        if predict[0] > THRESHOLD:
            pred = 1
        else:
            pred = 0
        sq._replace(pred_float = predict)
        sq._replace(pred_int = pred)
        # dict element sq is now obsolete, remove it
        sq._replace(sq = None)
    # print(f"name: {name}, first Sqr: {squares_dict[0].sq}, x: {squares_dict[0].x}, y: {squares_dict[0].y}")
    return name, squares_dict
    # report name, hot_pxl_list

if __name__ == "__main__":
    process()
