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
THRESHOLD = 0.4

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
datefmt='%m/%d/%Y %H:%M:%S',
filename='example.log',
filemode='w',
level=logging.WARNING)

def draw_sqr(name, frame, frame_n, x_list, y_list): #wanna list
    """takes a colour image/frame as np.array & x,y coordinates of square
    within this image. Draws box around square containing error,
    saves whole frame to disc as png, returns list of error frames"""
    # WRAP IN FOR LOOP OVER THE LIST OF (x, y) coming from the parameter
    for i in range(len(x_list)):
        cv2.rectangle(frame, (x_list[i], y_list[i]), (x_list[i]+FIX_IMG_SQR_SIZE, y_list[i]+FIX_IMG_SQR_SIZE), (0,255,0), 4)
    cv2.imwrite(f'frames/{name}{frame_n:04d}.png', frame)

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
    frame_n = 1
    print('model loaded')
    while(cap.isOpened()):
        #capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            squares_list = img_preprocess(frame)
            frame_n = frame_n+1
            print(f'enter video file, frame{frame_n}')
            x_list = []
            y_list = []
            for sq in squares_list:
                predict = predict_hot_pxl(sq.sq, model)
                if predict > threshold:
                    pred = 1
                    print('ERROR')
                    x_list.append(sq.y)
                    y_list.append(sq.x)
                    # draw square around error in frame:
                    # FIXME: save a square to a list of squares
                    continue
                else:
                    pred = 0
                    print('no error')
                # FIXME: draw_sqr(name, frame, frame_n, !!! PASS LIST INSTEAD !!! and rewrite the draw func to draw several squares sq.y, sq.x) 
                sq = sq._replace(pred_float = predict)
                sq = sq._replace(pred_int = pred)
                # dict element sq is now obsolete, remove it
                sq = sq._replace(sq = None)
            # save single frame with squares marking errors as png to disc:
            draw_sqr(name, frame, frame_n, x_list, y_list)
            frame_sqrs_list.append(sq)
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
    with open('model/model_strides_25_13-25-54.json', 'r') as f:
        model = model_from_json(f.read())
    # Load weights into the new model
    model.load_weights('model/bestmodel_weights_strides.hdf5')
    return model

def predict_hot_pxl(sqr, model):
    """takes a numpy array (colour image) size 64x64 and a ML model,
    returnes float number between 0 - 1 for hot pixel detection,
    for 0 no hot pixel detected, 1 hot pixel detected"""
    predict = model.predict(sqr.reshape(1,64,64,3))
    y_pred = predict[0][0]
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



if __name__ == "__main__":
    filename, debug = video_process()
    print(debug)
