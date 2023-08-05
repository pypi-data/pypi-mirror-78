import os

import gdown
from keras.layers import Conv2D, Activation, Input, Add, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Model


def network():
    inputs = Input(shape=(55, 47, 3))

    x = Conv2D(20, (4, 4), name='Conv1', activation='relu', input_shape=(55, 47, 3))(inputs)
    x = MaxPooling2D(pool_size=2, strides=2, name='Pool1')(x)
    x = Dropout(rate=1, name='D1')(x)

    x = Conv2D(40, (3, 3), name='Conv2', activation='relu')(x)
    x = MaxPooling2D(pool_size=2, strides=2, name='Pool2')(x)
    x = Dropout(rate=1, name='D2')(x)

    x = Conv2D(60, (3, 3), name='Conv3', activation='relu')(x)
    x = MaxPooling2D(pool_size=2, strides=2, name='Pool3')(x)
    x = Dropout(rate=1, name='D3')(x)

    x1 = Flatten()(x)
    fc11 = Dense(160, name='fc11')(x1)

    x2 = Conv2D(80, (2, 2), name='Conv4', activation='relu')(x)
    x2 = Flatten()(x2)
    fc12 = Dense(160, name='fc12')(x2)

    y = Add()([fc11, fc12])
    y = Activation('relu', name='deepid')(y)

    # Create model
    model = Model(inputs=[inputs], outputs=y)
    return model


def load_model(model_dir=None):
    from pathlib import Path
    if model_dir is None:
        model_dir = str(Path.home()) + '/.openfaces/weights/'
    output = os.path.join(model_dir, 'deepid_keras_weights.h5')
    if not os.path.isfile(output):
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        url = 'https://drive.google.com/uc?id=1uRLtBCTQQAvHJ_KVrdbRJiCKxU8m5q2J'
        gdown.download(url, output, quiet=False)

    model = network()
    model.load_weights(output)
    return model
