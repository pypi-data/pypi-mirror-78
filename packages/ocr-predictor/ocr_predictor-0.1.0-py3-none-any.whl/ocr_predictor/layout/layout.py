from detectron2.engine import DefaultPredictor
from detectron2.config import CfgNode
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2

import argparse
import os

class DL():
    def __init__(self, config):
        self.cfg = CfgNode.load_cfg(open(config['detectron']['config']))
        self.cfg.MODEL.WEIGHTS = config['detectron']['weights'] 

        self.classes = self.cfg.get('CLASSES')
        self.cfg.MODEL.DEVICE = config['device']
        self.predictor = DefaultPredictor(self.cfg)
        self.log = config['log']

    def predict(self, im):
        outputs = self.predictor(im)
        predictions = outputs['instances'].to('cpu')
        
        if self.log:
            self.visualize(im, predictions)

        boxes = predictions.pred_boxes.tensor.numpy() if predictions.has("pred_boxes") else None
        scores = predictions.scores.numpy() if predictions.has("scores") else None
        classes = predictions.pred_classes.numpy() if predictions.has("pred_classes") else None

        results = []
        for box, prob, clazz in zip(boxes, scores, classes):
            x1, y1, x2, y2 = box
            w = x2 - x1
            h = y2 - y1
            r = {'x': x1, 'y': y1, 'w': w, 'h': h, 'prob': prob, 'name': self.classes[clazz]}
            results.append(r)
        
        return results

    def visualize(self, im, predictions):
        metadata = MetadataCatalog.get('dump').set(thing_classes=self.classes)

        v = Visualizer(im[:, :, ::-1],
                       metadata=metadata, 
                       scale=1, 
        )
        
        v._default_font_size = 20
        v = v.draw_instance_predictions(predictions)
        new_im = v.get_image()[:, :, ::-1]

        cv2.imwrite('{}/layout.jpg'.format(self.log), new_im)
