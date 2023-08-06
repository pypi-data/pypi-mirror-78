import os
import zipfile

import gdown
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Flatten, Dense, Dropout
from keras.models import Model, Sequential


def network():
    num_classes = 7
    model = Sequential()

    # 1st convolution layer
    model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48, 48, 1)))
    model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))

    # 2nd convolution layer
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

    # 3rd convolution layer
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Flatten())

    # fully connected neural networks
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))

    # Create model
    model = Model(inputs=model.layers[0].input, outputs=model.layers[-1].output)
    return model


def load_model(model_dir=None):
    from pathlib import Path
    if model_dir is None:
        model_dir = str(Path.home()) + '/.openfaces/weights/'
    output = os.path.join(model_dir, 'facial_expression_model_weights.h5')
    if not os.path.isfile(output):
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        url = 'https://drive.google.com/uc?id=13iUHHP3SlNg53qSuQZDdHDSDNdBP9nwy'
        gdown.download(url, output + '.zip', quiet=False)
        with zipfile.ZipFile(output + '.zip', 'r') as zip_ref:
            zip_ref.extractall(model_dir)

    model = network()
    model.load_weights(output)
    return model
