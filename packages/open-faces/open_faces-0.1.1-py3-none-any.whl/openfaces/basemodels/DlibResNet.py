import bz2
import os

import dlib
import gdown
import numpy as np


class DlibResNet:
    def __init__(self, model_dir=None):
        from pathlib import Path
        if model_dir is None:
            model_dir = str(Path.home()) + '/.openfaces/weights/'
        output = os.path.join(model_dir, 'dlib_face_recognition_resnet_model_v1.dat')
        if not os.path.isfile(output):
            if not os.path.exists(model_dir):
                os.mkdir(model_dir)
            url = 'http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2'
            gdown.download(url, output + ".bz2", quiet=False)
            zipfile = bz2.BZ2File(output + ".bz2")
            data = zipfile.read()
            open(output, 'wb').write(data)

        model = dlib.face_recognition_model_v1(output)
        self.__model = model

    def predict(self, img_aligned):
        # functions.detectFace returns 4 dimensional images
        if len(img_aligned.shape) == 4:
            img_aligned = img_aligned[0]
        # functions.detectFace returns bgr images
        img_aligned = img_aligned[:, :, ::-1]  # bgr to rgb
        # deepface.detectFace returns an array in scale of [0, 1] but dlib expects in scale of [0, 255]
        if img_aligned.max() <= 1:
            img_aligned = img_aligned * 255
        img_aligned = img_aligned.astype(np.uint8)
        model = self.__model
        img_representation = model.compute_face_descriptor(img_aligned)
        img_representation = np.array(img_representation)
        img_representation = np.expand_dims(img_representation, axis=0)
        return img_representation
