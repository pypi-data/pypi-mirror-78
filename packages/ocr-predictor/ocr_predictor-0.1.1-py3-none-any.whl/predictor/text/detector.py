from PIL import Image
import io
from google.cloud import vision
import base64
from google.cloud.vision import types
import vietocr.tool.predictor as ocr
from vietocr.tool.config import Cfg

class TextDetector():

    def __init__(self, config):
        self.client = vision.ImageAnnotatorClient()

        vietocr_config = Cfg.load_config_from_file(config['vietocr']['config'])
        vietocr_config['weights'] = config['vietocr']['weights']
        vietocr_config['device'] = config['device']
        self.detector = ocr.Predictor(vietocr_config)

        self.log = config['log']

        self.i = 0

    def google_vision(self, img):
        img = Image.fromarray(img)
        output = io.BytesIO()
        img.save(output, format='JPEG')
        content = output.getvalue()

        content = types.Image(content=content)

        response = self.client.text_detection(image=content)
        texts = response.text_annotations
        if len(texts) > 0:
            return texts[0].description.rstrip(), 1.0
        else:
            return "", 0
    
    def vietocr(self, img):
        img = Image.fromarray(img)

        text = self.detector.predict(img)
        text = text.strip()

        return text, 1.0

    def predict(self, img):
#        return self.google_vision(img)
             
        return self.vietocr(img)
