import numpy as np
from .predict import Predictor,PredictConfigBase
from .dataset import load_image_files
import wk
import cv2


class TestConfigBase:
    TEST_DIR=None
    TEST_OUTPUT_DIR=None
    PREDICT_CONFIG=None
    predictor=None
    def __init__(self):
        if not self.TEST_OUTPUT_DIR:
            self.TEST_OUTPUT_DIR=self.TEST_DIR+'_test_out'
        wk.remake(self.TEST_OUTPUT_DIR)
        assert self.PREDICT_CONFIG or self.predictor
    def get_predictor(self):
        return self.predictor or Predictor(self.PREDICT_CONFIG)

def test(cfg):
    assert isinstance(cfg,TestConfigBase)
    fs=load_image_files(cfg.TEST_DIR,recursive=True)
    predictor=cfg.get_predictor()
    outFolder=wk.Folder(cfg.TEST_OUTPUT_DIR)
    res={}
    print('Num images: %s'%(len(fs)))
    for i,f in enumerate(fs):
        img=cv2.imread(f)
        cls,prob=predictor.predict(img)
        outFolder.openFolder(cls).eat(f)
        print(i,f,cls)
        res[f]=[cls,prob]
    return res

if __name__ == '__main__':
    test(TestConfigBase())