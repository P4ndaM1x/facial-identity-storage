import cv2
from pathlib import Path

HAAR_CASCADE_PATH = Path(Path(__file__).resolve().parent) / "haarcascade_frontalface_default.xml"

class FaceExtractor:
    def __init__(self, cascade_path=HAAR_CASCADE_PATH):
        self.cascade_path = cascade_path
        self.cascade_classifier = cv2.CascadeClassifier(str(cascade_path))

    def _get_box(self, img, top_correction=0.1):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        boxes = self.cascade_classifier.detectMultiScale(gray_img, 1.02, 2, minSize=(200,200))
        if len(boxes) == 0:
            raise ValueError("No faces detected")
        box = boxes[0]
        height = box[3]
        box[1] -= int(height * top_correction)
        box[3] += int(height * top_correction)
        return box

    def get_photo(self, file_path, top_correction=0.1):
        img = cv2.imread(filename=file_path)
        x, y, w, h = self._get_box(img, top_correction)
        return img[y:y+h, x:x+w]