
from wcf.packages.demo import test,TestConfigBase,PredictConfigBase

class PredictConfig(PredictConfigBase):

    INPUT_SIZE = (9*32,8*32)
    CLASSES_PATH = 'classes.txt'

class TestConfig(TestConfigBase):
    TEST_DIR='/home/ars/sda5/data/projects/烟分类/data/烟分类-val'
    TEST_OUTPUT_DIR=None
    PREDICT_CONFIG=PredictConfig()


if __name__ == '__main__':
    test(TestConfig())