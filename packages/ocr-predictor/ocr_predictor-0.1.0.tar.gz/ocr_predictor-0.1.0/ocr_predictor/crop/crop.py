from detectron2.engine import DefaultPredictor
from detectron2.config import CfgNode

from ocr_predictor.crop.utils import crop
import cv2

class Cropper():
    def __init__(self, config):
        self.cfg = CfgNode.load_cfg(open(config['crop']['config']))
        self.cfg.MODEL.WEIGHTS = config['crop']['weights'] 

        self.classes = self.cfg.get('CLASSES')
        self.cfg.MODEL.DEVICE = config['device']
        self.predictor = DefaultPredictor(self.cfg)
        
        self.log = config['log']

    def crop(self, im):
        outputs = self.predictor(im)
        predictions = outputs['instances'].to('cpu')

        boxes = predictions.pred_boxes.tensor.numpy() if predictions.has("pred_boxes") else None
        scores = predictions.scores.numpy() if predictions.has("scores") else None
        classes = predictions.pred_classes.numpy() if predictions.has("pred_classes") else None
        maskes = predictions.pred_masks.numpy() if predictions.has("pred_masks") else None

        results = []
        for mask, prob, clazz in zip(maskes, scores, classes):
            clzz = self.classes[clazz] 
            pred_order = int(clzz.split('_')[-1])
            
            crop_img = crop(im, mask, pred_order)

            r = {'img': crop_img, 'class':clzz[:-2]}
            results.append(r)
            
            if self.log:
                cv2.imwrite('{}/crop_{}.jpg'.format(self.log, len(results)), crop_img)                

        return results 
