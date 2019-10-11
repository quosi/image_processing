from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import regularizers
from keras import backend as K
from sklearn.metrics import classification_report
from keras.layers.normalization import BatchNormalization

from time import gmtime, strftime
import os, random
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
This script builds a image classification models to detect pixes-errors
in video footage.
steps to do first:
- created a data/ folder
- created train/ and validation/ subfolders inside data/
- created clean/ and error/ subfolders inside train/ and validation/
- put the clean pictures index 0-999 in data/train/clean
- put the clean pictures index 1000-1400 in data/validation/clean

- put the error pictures index 12500-13499 in data/train/error
- put the error pictures index 13500-13900 in data/validation/error
So that we have 1000 training examples for each class, and 400 validation examples for each class.
In summary, this is our directory structure:

data/
    train/
        error/
            error001.jpg
            error002.jpg
            ...
        clean/
            clean001.jpg
            clean002.jpg
            ...
    validation/
        error/
            error001.jpg
            error002.jpg
            ...
        clean/
            clean001.jpg
            clean002.jpg
            ...
'''



if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

def model_set_up(epochs, batch_size, dropout_rate):
    # dimensions of input images
    img_width, img_height = 64, 64

    train_data_dir = 'keras_cnn/train/'
    validation_data_dir = 'keras_cnn/validation/'
    test_dir = 'keras_cnn/test/'
    nb_train_samples = 375000
    nb_validation_samples = 160000
    epochs = epochs
    batch_size = batch_size
    location = os.getcwd()

    n_images = nb_train_samples + nb_validation_samples
    print(f"[INFO] loading {n_images} images from '{location.split('/')[-1]}' ...")

    K.clear_session()
    model = Sequential()
    # padding anschalten um die ecken zu checken
    model.add(Conv2D(8, (3, 3), input_shape=input_shape, strides=(2,2), padding='same', kernel_regularizer=regularizers.l2(0.01), use_bias=True))
    #odel.add(BatchNormalization(epsilon=1e-06, mode=0, momentum=0.9, weights=None))
    model.add(Activation('relu'))

    model.add(Conv2D(8, (3, 3), padding='same', strides=(2,2), kernel_regularizer=regularizers.l2(0.01), use_bias=True))
    #model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(Dropout(dropout_rate))
    model.add(Conv2D(32, (3, 3), use_bias=True, strides=(2,2), kernel_regularizer=regularizers.l2(0.01),))
    #model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(Flatten())
    model.add(Dense(64))
    #model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    opt = Adam(lr=1e-4, decay=1e-4 / epochs)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

    # checkpoints
    checkpoint = ModelCheckpoint(filepath='keras_cnn/model/bestmodel_weights_strides.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    earlystopper = EarlyStopping(monitor='val_loss', patience=4, verbose=1)
    callbacks_list = [checkpoint]
    model.summary()

    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(horizontal_flip=True)
    # this is the augmentation configuration we will use for testing:
    test_datagen = ImageDataGenerator(horizontal_flip=True)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        color_mode="rgb",
        batch_size=batch_size,
        class_mode='binary')

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        color_mode="rgb",
        batch_size=batch_size,
        class_mode='binary')

    hist = model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=nb_validation_samples // batch_size,
        callbacks=[checkpoint])

    ti = strftime("%d_%H-%M-%S", gmtime())

    # save eights to HDF5
    model.save_weights(f'keras_cnn/model/cnn-model_strides_{ti}.h5')
    print("Saved model to disk")
    # save model to JSON
    with open(f"keras_cnn/model/model_strides_{ti}.json", "w") as json_file:
        json_file.write(model.to_json())

    # evaluate the network
    print("[INFO] evaluating network...")
    # plot the training loss and accuracy
    epochs = len(list(hist.history.values())[0])
    fig = plt.figure()
    plt.plot(np.arange(0, epochs), hist.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), hist.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epochs), hist.history["acc"], label="train_acc")
    plt.plot(np.arange(0, epochs), hist.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy on Dataset")
    plt.xlabel(f"Epoch (max. {epochs})")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig(f"keras_cnn/plots/plot_strides_{ti}.png")
    plt.show()

    test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    color_mode="rgb",
    shuffle = False,
    class_mode='binary',
    batch_size=1)

    filenames = test_generator.filenames
    nb_samples = len(filenames)
    predict = model.predict_generator(test_generator,steps = nb_samples)
    y_pred = [i[0].round() for i in predict]

    # set y_true for test data
    images_clean = os.listdir('keras_cnn/test/clean')
    images_error = os.listdir('keras_cnn/test/error')
    y_clean = np.zeros(len(images_clean))
    y_error =  np.ones(len(images_error))
    y_true = list(np.concatenate((y_clean, y_error), axis=0))
    filenames = list(np.concatenate((images_clean, images_error), axis=0))
    loc_folder = ['/clean/']*len(images_clean)+['/error/']*len(images_error)
    loc_images = list(np.concatenate((images_clean, images_error), axis=0))
    src_img=[]
    for i in range(len(loc_folder)):
        src_img.append(loc_folder[i] + loc_images[i])
    y_clean = np.zeros(len(images_clean))
    y_error = np.ones(len(images_error))
    y_true = list(np.concatenate((y_clean, y_error), axis=0))

    print(classification_report(y_true, y_pred))

    result = dict(zip([each[0] for each in predict], src_img))
    df = pd.DataFrame(result, index=range(1))
    df = df.T.reset_index()
    df.columns = ['y_pred', 'file']
    df.to_csv(f'keras_cnn/result_csv/result_strides_{ti}.csv', index=False)
model_set_up()
