import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random

LOCATION = '../images/'
location_src = LOCATION + 'movie_pics/'
location_squares = LOCATION + 'squares/'
location_squares_error = LOCATION + 'error_squares/'

images = os.listdir(location_src)
n_images = len(images)
print(f"[INFO] loading {n_images} images from {location_src}...")
data = []
labels = []
b = 0

for image in images:
    label = image.split('.')[-2]
    print(label)
    labels.append(label)

    img = Image.open('images/movie_pics/'+image)
    img = np.array(img)
    for x in range(0, img.shape[0], 64):
        xvon = x
        xbis = x+64
        if xvon > img.shape[0]-64:
            xvon = img.shape[0]-64
            xbis = img.shape[0]
        for y in range(0, img.shape[1], 64):
            yvon = y
            ybis = y+64
            if y+64 > img.shape[1]:
                yvon = img.shape[1]-64
                ybis = img.shape[1]

            square = img[xvon:xbis, yvon:ybis,:]
            Image.fromarray(square).convert("RGB").save(location_squares+label+"_"+str(x)+"_"+str(y)+".png")

            for i in range(random.choice([1, 2, 3])):
                #Add some hot pixel errors
                square[np.random.randint(low=0,high=64),np.random.randint(low=0,high=64)]= np.random.randint(low=200,high=255)
                square[np.random.randint(low=0,high=64),np.random.randint(low=0,high=64)]= np.random.randint(low=0,high=10)
            Image.fromarray(square).convert("RGB").save(location_squares_error+label+"_"+str(x)+"_"+str(y)+".png")

            b = b+1
            if b > 3:
                break
