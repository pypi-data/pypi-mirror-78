import os
import zipfile

import gdown
from keras.layers import Convolution2D, LocallyConnected2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Model, Sequential


def network():
    model = Sequential()
    model.add(Convolution2D(32, (11, 11), activation='relu', name='C1', input_shape=(152, 152, 3)))
    model.add(MaxPooling2D(pool_size=3, strides=2, padding='same', name='M2'))
    model.add(Convolution2D(16, (9, 9), activation='relu', name='C3'))
    model.add(LocallyConnected2D(16, (9, 9), activation='relu', name='L4'))
    model.add(LocallyConnected2D(16, (7, 7), strides=2, activation='relu', name='L5'))
    model.add(LocallyConnected2D(16, (5, 5), activation='relu', name='L6'))
    model.add(Flatten(name='F0'))
    model.add(Dense(4096, activation='relu', name='F7'))
    model.add(Dropout(rate=0.5, name='D0'))
    model.add(Dense(8631, activation='softmax', name='F8'))

    # Create model
    model = Model(inputs=model.layers[0].input, outputs=model.layers[-3].output)
    return model


def load_model(model_dir=None):
    from pathlib import Path
    if model_dir is None:
        model_dir = str(Path.home()) + '/.openfaces/weights/'
    output = os.path.join(model_dir, 'VGGFace2_DeepFace_weights_val-0.9034.h5')
    if not os.path.isfile(output):
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        url = 'https://github.com/swghosh/DeepFace/releases/download/weights-vggface2-2d-aligned/\
        VGGFace2_DeepFace_weights_val-0.9034.h5.zip'
        gdown.download(url, output + ".zip", quiet=False)
        with zipfile.ZipFile(output + ".zip", 'r') as zip_ref:
            zip_ref.extractall(model_dir)

    model = network()
    model.load_weights(output)
    return model
