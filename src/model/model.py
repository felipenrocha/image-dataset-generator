import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import os
from keras.optimizers import SGD

# from sklearn.metrics import confusion_matrix, classification_report


# model for training the dogs and cats dataset, scrapped from bing


import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Activation, BatchNormalization, GlobalAveragePooling2D, Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.applications.vgg16 import VGG16
from dotenv.main import load_dotenv
import pandas as pd
load_dotenv()

MODEL_NAME = os.environ['MODEL_NAME']


# load datasets paths
train_dataset_path = '../../' + MODEL_NAME + '/seg_train'
validation_dataset_path = '../../' + MODEL_NAME + '/seg_test'
num_classes = len(os.listdir(train_dataset_path))
# resize images to 1/3:

IMG_WIDTH = 256
IMG_HEIGHT = 256

# SIZE OF BATCH

BATCH_SIZE = 32


def main():

    datagen = ImageDataGenerator(rescale=1.0/255.0)

    train_it = datagen.flow_from_directory(train_dataset_path,
                                           class_mode='categorical', batch_size=BATCH_SIZE, target_size=(IMG_HEIGHT, IMG_WIDTH))
    test_it = datagen.flow_from_directory(validation_dataset_path,
                                          class_mode='categorical', batch_size=BATCH_SIZE, target_size=(IMG_HEIGHT, IMG_WIDTH))
    labels = {value: key for key,
              value in train_it.class_indices.items()}

    print("Label Mappings for classes present in the training and validation datasets\n")
    for key, value in labels.items():
        print(f"{key} : {value}")

    model = create_model()
    datagen = ImageDataGenerator(rescale=1.0/255.0)
    # prepare iterator
    train_it = datagen.flow_from_directory(train_dataset_path,
                                           class_mode='categorical', batch_size=BATCH_SIZE, target_size=(IMG_HEIGHT, IMG_WIDTH))
    test_it = datagen.flow_from_directory(validation_dataset_path,
                                          class_mode='categorical', batch_size=BATCH_SIZE, target_size=(IMG_HEIGHT, IMG_WIDTH))
    # fit model
    history = model.fit(train_it,
                        validation_data=test_it, epochs=50, verbose=1)
    # evaluate model

    model.save('../../datasets/models/' + MODEL_NAME + '/')
    hist_df = pd.DataFrame(history.history)

    hist_csv_file = '../../datasets/history' + MODEL_NAME + '.csv'
    with open(hist_csv_file, mode='w') as f:
        hist_df.to_csv(f)


def create_model():
    # model for multiple classes (labels)
    model = Sequential([
        Conv2D(filters=128, kernel_size=(5, 5), padding='valid',
               input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Conv2D(filters=64, kernel_size=(3, 3), padding='valid',
               kernel_regularizer=l2(0.00005)),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Conv2D(filters=32, kernel_size=(3, 3), padding='valid',
               kernel_regularizer=l2(0.00005)),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Flatten(),

        Dense(units=256, activation='relu'),
        Dropout(0.5),
        Dense(units=num_classes, activation='softmax')
    ])
    opt = Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss=CategoricalCrossentropy(), metrics=['accuracy'])
    return model




if __name__ == "__main__":
    main()
