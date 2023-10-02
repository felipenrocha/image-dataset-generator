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
from tensorflow.keras.layers import Activation,MaxPool2D, BatchNormalization, GlobalAveragePooling2D, Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.applications.vgg16 import VGG16
from dotenv.main import load_dotenv
import pandas as pd
load_dotenv()


from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


def fix_gpu():
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)




BASE_PATH = os.getcwd() + '\\'
MODEL_NAME = os.environ['MODEL_NAME'] 



# load datasets paths
train_dataset_path = BASE_PATH + MODEL_NAME + '\seg_train'
validation_dataset_path = BASE_PATH + MODEL_NAME + '\seg_test'
num_classes = len(os.listdir(train_dataset_path))
print('num_classes',num_classes)
# resize images to 1/3:

IMG_WIDTH = 256
IMG_HEIGHT = 256

# SIZE OF BATCH

BATCH_SIZE = 32


def main():
    fix_gpu()
    datagen = ImageDataGenerator(rescale=1.0/255.0)

    train_it = datagen.flow_from_directory(train_dataset_path,
                                           class_mode='binary', batch_size=BATCH_SIZE, target_size=(IMG_HEIGHT, IMG_WIDTH))
    test_it = datagen.flow_from_directory(validation_dataset_path,
                                          class_mode='binary', batch_size=BATCH_SIZE, target_size=(IMG_HEIGHT, IMG_WIDTH))
    labels = {value: key for key,
              value in train_it.class_indices.items()}

    print("Label Mappings for classes present in the training and validation datasets\n")
    for key, value in labels.items():
        print(f"{key} : {value}")

    model = create_model()
  
    
    model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

    # fit model
    history = model.fit_generator(train_it,
         steps_per_epoch = 250,
         epochs = 50,
         validation_data = test_it
       
         )
    # evaluate model

    model.save(BASE_PATH + 'datasets\models\\' + MODEL_NAME + '\\')
    hist_df = pd.DataFrame(history.history)

    hist_csv_file = BASE_PATH + 'datasets\history\\' + MODEL_NAME + '.csv'
    with open(hist_csv_file, mode='w') as f:
        hist_df.to_csv(f)
    return

def create_model():
    # model for multiple classes (labels)
    model = Sequential()
    # Convolutional layer and maxpool layer 1
    model.add(Conv2D(32,(3,3),activation='relu',input_shape=(150,150,3)))
    model.add(MaxPool2D(2,2))

    # Convolutional layer and maxpool layer 2
    model.add(Conv2D(64,(3,3),activation='relu'))
    model.add(MaxPool2D(2,2))

    # Convolutional layer and maxpool layer 3
    model.add(Conv2D(128,(3,3),activation='relu'))
    model.add(MaxPool2D(2,2))

    # Convolutional layer and maxpool layer 4
    model.add(Conv2D(128,(3,3),activation='relu'))
    model.add(MaxPool2D(2,2))

    # This layer flattens the resulting image array to 1D array
    model.add(Flatten())

    # Hidden layer with 512 neurons and Rectified Linear Unit activation function 
    model.add(Dense(512,activation='relu'))

    # Output layer with single neuron which gives 0 for Cat or 1 for Dog 
    #Here we use sigmoid activation function which makes our model output to lie between 0 and 1
    model.add(Dense(1,activation='sigmoid'))
    return model


if __name__ == "__main__":
    main()
