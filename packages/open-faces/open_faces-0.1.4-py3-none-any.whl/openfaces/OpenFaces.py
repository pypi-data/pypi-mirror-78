import os
import warnings
from pathlib import Path
import cv2
import dlib
import numpy as np
from keras.preprocessing import image

from openfaces.attributes import Age, Gender, Race, Emotion

warnings.filterwarnings("ignore")


def convert(img, target_size=(224, 224), grayscale=False):
    if grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, target_size)
    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis=0)
    img_pixels /= 255
    return img_pixels


class OpenFaces:

    def __init__(self, model_dir=None):
        self.models = {}
        self._load_face_model(model_dir)
        self._load_attribute_model(model_dir)

    def _load_face_model(self, model_dir):
        if model_dir is None:
            model_dir = str(Path.home()) + '/.openfaces/weights/'
        output = os.path.join(model_dir, 'mmod_human_face_detector.dat')
        self.cnn_face_detector = dlib.cnn_face_detection_model_v1(output)
        self.shape_predictor = dlib.shape_predictor(os.path.join(model_dir, 'shape_predictor_68_face_landmarks.dat'))

    def _load_attribute_model(self, model_dir):
        self.models["emotion"] = Emotion.load_model(model_dir)
        self.models["age"] = Age.load_model(model_dir)
        self.models["gender"] = Gender.load_model(model_dir)
        self.models["race"] = Race.load_model(model_dir)

    def face_locations(self, img, number_of_times_to_upsample=1):
        def _rect_to_css(rect):
            return rect.top(), rect.right(), rect.bottom(), rect.left()

        def _trim_css_to_bounds(css, image_shape):
            return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

        return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in
                self.cnn_face_detector(img, number_of_times_to_upsample)]

    def face_alignment(self, img, locations, size=224):
        def _css_to_rect(css):
            return dlib.rectangle(css[3], css[0], css[1], css[2])

        faces = dlib.full_object_detections()
        for location in locations:
            faces.append(self.shape_predictor(img, _css_to_rect(location)))
        return dlib.get_face_chips(img, faces, size)

    def predict(self, img):
        resp_obj = {}
        emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        img_48 = convert(img, target_size=(48, 48), grayscale=True)
        emotion_predictions = self.models["emotion"].predict(img_48)[0, :]
        resp_obj['emotion'] = emotion_labels[np.argmax(emotion_predictions)]

        img = convert(img, target_size=(224, 224), grayscale=False)
        age_predictions = self.models["age"].predict(img)[0, :]
        resp_obj['age'] = Age.convert(age_predictions)

        gender_prediction = self.models["gender"].predict(img)[0, :]
        if np.argmax(gender_prediction) == 0:
            gender = "Woman"
        elif np.argmax(gender_prediction) == 1:
            gender = "Man"
        resp_obj['gender'] = gender

        race_predictions = self.models["race"].predict(img)[0, :]
        race_labels = ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
        resp_obj['race'] = race_labels[np.argmax(race_predictions)]

        return resp_obj


if __name__ == "__main__":
    import cv2
    from openfaces import OpenFaces

    model = OpenFaces.OpenFaces()

    path = "img2.jpg"
    src = cv2.imread(path)
    rects = model.face_locations(src)
    news = model.face_alignment(src, rects)
    for i in range(len(news)):
        cv2.imwrite("__%s.png" % i, news[i])
        result = model.predict(news[i])
        print(result)
