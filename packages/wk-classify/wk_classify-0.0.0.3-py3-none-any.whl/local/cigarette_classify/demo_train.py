
from wcf.packages.demo import train, TrainValConfigBase, t,EasyTransform


class Config(TrainValConfigBase):
    MODEL_TYPE = 'shufflenet_v2_x0_5'
    # MODEL_TYPE = 'resnet18'
    GEN_CLASSES_FILE = True
    USE_tqdm_TRAIN = True
    INPUT_SIZE = (9 * 32, 8 * 32)
    BATCH_SIZE = 64
    NUM_EPOCHS = 200
    BALANCE_CLASSES = False
    VAL_INTERVAL = 1
    WEIGHTS_SAVE_INTERVAL = 0.2
    WEIGHTS_INIT = 'weights/training/model_best.pkl'
    # WEIGHTS_INIT = '/home/ars/sda6/work/play/wk-classify/local/weights/training/model_best_[epoch=1&acc=0.5938].pkl'
    TRAIN_DIR = '/home/ars/sda5/data/projects/烟分类/data/烟分类-train'
    VAL_DIR = '/home/ars/sda5/data/projects/烟分类/data/烟分类-val'
    # VAL_DIR = '/home/ars/sda5/data/projects/烟分类/data/烟分类-train'
    val_transform = EasyTransform([
        t.Resize(INPUT_SIZE[::-1]),
        t.SaveToDir('data/test'),
        t.ToTensor(),
    ])
    train_transform = EasyTransform([
        t.ColorJitter(brightness=0.2, contrast=0.1, saturation=0.1, hue=0.1),
        # t.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05),
        t.RandomHorizontalFlip(),
        t.RandomVerticalFlip(),
        t.RandomRotate(360),
        t.RandomTranslate(30),
        t.RandomBlur(p=0.3, radius=1),
        t.RandomSPNoinse(p=0.3),
        *val_transform,
    ])
    # def get_model(self, num_classes=None):
        # return TwoLayerNet(17)
        # return LightNet(17)



if __name__ == '__main__':
    cfg = Config()
    train(cfg)
    # res=val(cfg)
    # print(res)
