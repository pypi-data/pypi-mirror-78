import base64
import hashlib
import os
from pathlib import Path

import cv2
import numpy as np


def load_base64(uri):
    data = uri.split(',')[1]
    data = np.fromstring(base64.b64decode(data), np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img


def get_file_hash(file):
    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(65536)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(65536)
    return file_hash.hexdigest()


def initialize():
    home = str(Path.home())
    if not os.path.exists(home + "/.openfaces"):
        os.mkdir(home + "/.openfaces")
        print("Directory ", home, "/.openfaces created")

    if not os.path.exists(home + "/.openfaces/weights"):
        os.mkdir(home + "/.openfaces/weights")
        print("Directory ", home, "/.openfaces/weights created")


def find_threshold(model_name, distance_metric):
    threshold = 0.40
    if model_name == 'VGGFace':
        if distance_metric == 'cosine':
            threshold = 0.40
        elif distance_metric == 'euclidean':
            threshold = 0.55
        elif distance_metric == 'euclidean_l2':
            threshold = 0.75
    elif model_name == 'OpenFace':
        if distance_metric == 'cosine':
            threshold = 0.10
        elif distance_metric == 'euclidean':
            threshold = 0.55
        elif distance_metric == 'euclidean_l2':
            threshold = 0.55
    elif model_name == 'FaceNet':
        if distance_metric == 'cosine':
            threshold = 0.40
        elif distance_metric == 'euclidean':
            threshold = 10
        elif distance_metric == 'euclidean_l2':
            threshold = 0.80
    elif model_name == 'DeepFace':
        if distance_metric == 'cosine':
            threshold = 0.23
        elif distance_metric == 'euclidean':
            threshold = 64
        elif distance_metric == 'euclidean_l2':
            threshold = 0.64
    elif model_name == 'DeepID':
        if distance_metric == 'cosine':
            threshold = 0.015
        elif distance_metric == 'euclidean':
            threshold = 45
        elif distance_metric == 'euclidean_l2':
            threshold = 0.17
    elif model_name == 'Dlib':
        if distance_metric == 'cosine':
            threshold = 0.07
        elif distance_metric == 'euclidean':
            threshold = 0.60
        elif distance_metric == 'euclidean_l2':
            threshold = 0.60
    return threshold
