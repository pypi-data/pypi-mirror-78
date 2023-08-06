import yaml
import torch
import torch.nn as nn
from torchvision import transforms, models

class DC():
    def __init__(self, cfg):
        self.mcfg = cfg

        self.cfg = config = yaml.safe_load(open(cfg['resnet']['config']))
        self.classes = self.cfg['CLASSES']
        self.cfg['MODEL']['WEIGHTS'] = cfg['resnet']['weights']
        self.device = self.mcfg['device']

        self.build_model()

    def build_model(self):
        self.transformer = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((self.cfg['INPUT']['SIZE'], self.cfg['INPUT']['SIZE'])),
            transforms.ToTensor(),
            transforms.Normalize(self.cfg['MODEL']['PIXEL_MEAN'], self.cfg['MODEL']['PIXEL_STD'])
            ])

        model = models.resnet18(pretrained=True)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, self.cfg['MODEL']['NUM_CLASSES'])
        model.load_state_dict(torch.load(self.cfg['MODEL']['WEIGHTS'], map_location=torch.device(self.device)))
        model.eval()

        model.to(self.device)

        self.model = model

    def predict(self, img):
        img = self.transformer(img).unsqueeze_(0)
        img = img.to(self.device)
    
        with torch.no_grad():
            outputs = self.model(img)
        _, preds = torch.max(outputs, 1)
        pred = self.classes[preds.item()]

        return pred

