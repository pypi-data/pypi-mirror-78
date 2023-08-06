import numpy as np
from torchvision import transforms
from wpcv.utils.data_aug import img_aug, random_float_generator
from wpcv.utils.ops import pil_ops
from wcf.packages.demo import Predictor,PredictConfigBase,load_image_files,test,TestConfigBase
from wcf.packages.resnet.dataset import load_image_files
from wcf.packages.resnet.testing import test,TestConfigBase
from wk import remake
import wk
import cv2

class PredictConfig(PredictConfigBase):

    INPUT_SIZE = (9*32,8*32)
    CLASSES_PATH = 'classes.txt'



def demo():
    predictor = Predictor(PredictConfig)
    f=''
    img=cv2.imread(f)
    y,prob=predictor.predict(img)
    print(y,prob)

if __name__ == '__main__':
    demo()