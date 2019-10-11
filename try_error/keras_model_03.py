from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
K.clear_session()

import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import random

LOCATION = 'images/'
src_error = LOCATION + 'error_squares/'   # y-lable = 1
src_clean = LOCATION + 'squares/'         # y-lable = 0
location_keras = LOCATION + 'keras/'

# set y-labels for the 2 types of image data
images_clean = os.listdir(src_clean)
y_clean = np.zeros(len(images_clean))
print(len(y_clean))

images_error = os.listdir(src_error)
print(len(images_error))

y_error =  np.ones(len(images_error))

images = images_clean + images_error
# y_labels = np.concatenate((np.ones(len(images_error)), np.zeros(len(images_clean))), axis=0)
y_labels = np.concatenate((np.ones(500), np.zeros(500)), axis=0)

n_images = len(images)

if(n_images == len(y_labels)):
    print(f"[INFO] loading {n_images} images from {src_error+src_clean}...")
else: print('Number of images and labels are differnt!')

input_shape = (0,0,0)
X_data = np.array
#print(location_src+image)
for image in images_clean[:500]:
    img = Image.open(src_clean+image)
    img = np.array(img)
    X_data.append(img)
    input_shape = img.shape

for image in images_error[:500]:
    img = Image.open(src_error+image)
    img = np.array(img)
    X_data.append(img)
    input_shape = img.shape

input_shape = img.shape
print(input_shape)


# CNN model setup
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print(model.summary())

# split  X, y data to fit model

X = np.array(X_data)
y = y_labels
print(len(X))
X[0].shape
print(y[:10])
len(y)

hist = model.fit(X, y, epochs=20, batch_size = 500, validation_split=0.2, verbose=1)
model.save_weights('first_try.h5')

%matplotlib inline
plt.figure(figsize=(10, 8))
plt.plot(hist.history['accuracy'], label='accuracy')
plt.plot(hist.history['val_accuracy'], label='val_accuracy')

score = model.evaluate(X, y, batch_size=4)
print(score)
print(model.predict(X))
