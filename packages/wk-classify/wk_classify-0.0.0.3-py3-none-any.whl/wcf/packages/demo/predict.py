import torch
import numpy as np
import os,shutil,glob
from PIL import Image
import cv2
from torchvision import transforms
import logging
from .network import load_model


class PredictConfigBase:
    MODEL_TYPE='resnet18'
    CLASSES_PATH=None
    CLASSES=None
    INPUT_SIZE=(224,224)
    transform= transforms.Compose([
            transforms.Resize(INPUT_SIZE[::-1]),
            transforms.ToTensor(),
        ])
    DEVICE=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    WEIGHTS_PATH='weights/model.pkl'
    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)
        if self.CLASSES_PATH :
            if os.path.exists(self.CLASSES_PATH):
                with open(self.CLASSES_PATH,'r') as f:
                    self.CLASSES=f.read().strip().split('\n')
            else:
                logging.warning('CLASSES_PATH is given but does not exist.')
        assert self.CLASSES
        assert self.WEIGHTS_PATH and os.path.exists(self.WEIGHTS_PATH)
        self.model=self.get_model()
        self.model.load_state_dict(torch.load(self.WEIGHTS_PATH))
        self.model.to(self.DEVICE)
        self.model.eval()
    def get_model(self):
        return load_model(self.MODEL_TYPE,num_classes=len(self.CLASSES))



class Predictor:
    def __init__(self, cfg):
        assert isinstance(cfg,PredictConfigBase)
        self.device=cfg.DEVICE
        self.model=cfg.model
        self.transform=cfg.transform
        self.classes=cfg.CLASSES

    def predict(self,img):
        if isinstance(img,str):
            img=cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img=Image.fromarray(img)
        elif not isinstance(img,Image.Image):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
        im=img
        im = self.transform(im).float()
        im = torch.tensor(im).unsqueeze(0)
        im = im.to(self.device)
        y = self.model(im)
        y=torch.softmax(y,dim=1)
        prob,pred=torch.max(y,dim=1)
        y = int(pred)
        prob=float(prob)
        return self.classes[y] ,prob


