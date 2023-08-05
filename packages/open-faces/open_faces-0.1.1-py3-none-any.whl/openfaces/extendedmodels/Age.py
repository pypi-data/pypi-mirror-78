import os

import gdown
import numpy as np
from keras.layers import Convolution2D, Flatten, Activation
from keras.models import Model, Sequential

from openfaces.basemodels import VGGFace


def network():
    model = VGGFace.network()

    classes = 101
    base_model = Sequential()
    base_model = Convolution2D(classes, (1, 1), name='predictions')(model.layers[-4].output)
    base_model = Flatten()(base_model)
    base_model = Activation('softmax')(base_model)

    model = Model(inputs=model.input, outputs=base_model)
    return model


def load_model(model_dir=None):
    from pathlib import Path
    if model_dir is None:
        model_dir = str(Path.home()) + '/.openfaces/weights/'
    output = os.path.join(model_dir, 'age_model_weights.h5')
    if not os.path.isfile(output):
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        url = 'https://drive.google.com/uc?id=1YCox_4kJ-BYeXq27uUbasu--yz28zUMV'
        gdown.download(url, output, quiet=False)

    model = network()
    model.load_weights(output)
    return model


def convert(age_predictions):
    output_indexes = np.array([i for i in range(0, 101)])
    age = np.sum(age_predictions * output_indexes)
    return age
