"""
Interface script to a subsystem of I/O operations
Facade defines a higher-level interface that makes te Error Classifier easier
to use.
"""
import os, sys, random, collections, logging, cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
# from tensorflow.keras.models import model_from_json # for ATOM and every other sys
from keras.models import model_from_json              # for VisualStudioCode
from sklearn.metrics import classification_report
from time import gmtime, strftime

PATH = os.getcwd()
INPUTPATH = str(os.getcwd()) + '/uploads/'
FILE = os.listdir(INPUTPATH)[0]

FIX_IMG_SQR_SIZE = 64
SQ_OUT = collections.namedtuple('SQ_OUT',['sq', 'x', 'y', 'pred_float', 'pred_int'])
THRESHOLD = 0.6

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
datefmt='%m/%d/%Y %H:%M:%S',
filename='example.log',
filemode='w',
level=logging.WARNING)

def video_process(threshold=THRESHOLD, inputpath=INPUTPATH, file=FILE):
    """reads (max.10sec!) video file and stores every frame as PNG image for processing
    applies image segmentation & prediction for pixel error detection"""
    #create video capture object
    cap = cv2.VideoCapture(f'{inputpath}{file}')
    name = file.split('/')[-1].split('.')[0]
    frame_sqrs_list = []
    if (cap.isOpened()==False):
        logging.error('Error opening video stream or file')
    model = load_model()
    while(cap.isOpened()):
        #capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            squares_list = img_preprocess(frame)
            # optional: save squares
            #Image.fromarray(square).convert("RGB").save(location_squares+label+"_"+str(x)+"_"+str(y)+".png")
            for sq in squares_list:
                predict = predict_hot_pxl(sq.sq, model)
                if predict[0] > threshold:
                    pred = 1
                else:
                    pred = 0
                sq = sq._replace(pred_float = predict[0])
                sq = sq._replace(pred_int = pred)
                # dict element sq is now obsolete, remove it
                sq = sq._replace(sq = None)
            # save single frames in list and as png to disc:
            frame_sqrs_list.append(sq)
            #Image.fromarray(frame).save(f"frames/{name}_{i}.png")
        # Break the loop
        else:
            break
    return name, frame_sqrs_list

def img_in(filename):
    """read one colour image from filename,
    return image name and image as numpy array"""
    temp_img = Image.open(filename)
    img = np.array(temp_img)
    name = filename.split('.')[-2]
    return name, img

def img_preprocess(img):
    """cut numpy array (colour image) into squares of 64x64 (FIX_IMG_SQR_SIZE),
    return squares with associated, x and y coordinates in a dictionary."""
    squares = []
    x_size = img.shape[0]
    assert x_size >= FIX_IMG_SQR_SIZE
    y_size = img.shape[1]
    assert y_size >= FIX_IMG_SQR_SIZE
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
            squares.append(SQ_OUT(square, xstart, ystart, 3.0, 3))
    return squares

def load_model():
    """loding predefined CNN model and weights,
    retuns pretrained CNN model"""
    # Model reconstruction from JSON file
    with open('model/model_strides_11-24-50.json', 'r') as f:
        model = model_from_json(f.read())
    # Load weights into the new model
    model.load_weights('model/cnn-model_strides_11-24-50.h5')
    return model

def predict_hot_pxl(sqr, model):
    """takes a numpy array (colour image) size 64x64 and a ML model,
    returnes float number between 0 - 1 for hot pixel detection,
    for 0 no hot pixel detected, 1 hot pixel detected"""
    predict = model.predict(sqr.reshape(1,64,64,3))
    y_pred = [i[0] for i in predict]
    return y_pred

def round_pred_at_threshold(squares_dict, threshold=THRESHOLD):
    """rounding float numbers of each pred_float element from namedtuple type SQ_OUT,
    returns 0 or 1 depending on THRESHOLD value"""
    for sq in squares_dict:
        predict = sq.predict
        if predict < threshold:
            sq.replace(pred_int = 0)
        else:
            sq.replace(pred_int = 1)
    return squares_dict

# def report(sqrs_tuple):
#     """identifies frames containing errors by looking for pred_int = 1,
#     draws box around square containing error, saves whole frame as png,
#     returns list of error frames"""
#     for image in images:
#         for squares in image:
#             for sq in squares:
#                 if sq.pred_int == 1:
#                     pass


    return frame_list

if __name__ == "__main__":
    filename, debug = video_process()
    print(debug)
