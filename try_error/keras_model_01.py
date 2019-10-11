from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
#from keras.preprocessing import image
import keras.applications.resnet50 as resnet50
import keras.applications.xception as xception
import keras.applications.inception_v3 as inception_v3

import numpy as np

import os
from PIL import Image
import matplotlib.pyplot as plt
import random

LOCATION = 'images/'
location_src = LOCATION + 'error_squares/'
location_keras = LOCATION + 'keras/'
images = os.listdir(location_src)

n_images = len(images)
print(f"[INFO] loading {n_images} images from {location_src}...")

datagen = ImageDataGenerator(
        rotation_range=0,
        width_shift_range=0.0,
        height_shift_range=0.0,
        shear_range=0.0,
        zoom_range=0.0,
        horizontal_flip=FALSE,
        fill_mode='nearest')

for image in images:
    img = load_img(location_src+image)
    img = np.array(img)
    print(img.shape())

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
i = 0
for batch in datagen.flow(x, batch_size=1, save_to_dir='images/movie_pics/keras', save_prefix='clean', save_format='png'):
    i += 1
    if i > 20:
        break  # otherwise the generator would loop indefinitely
