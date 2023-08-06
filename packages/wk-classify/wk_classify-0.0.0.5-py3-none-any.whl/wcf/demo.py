
from wcf import train, TrainValConfigBase, val,t,EasyTransform,models_names


class Config(TrainValConfigBase):
    MODEL_TYPE = models_names.shufflenet_v2_x0_5
    # MODEL_TYPE = models_names.resnet18
    TAG = '[%s]'%(MODEL_TYPE)
    GEN_CLASSES_FILE = True
    USE_tqdm_TRAIN = True
    INPUT_SIZE = (252,196)
    BATCH_SIZE = 64
    NUM_EPOCHS = 200
    BALANCE_CLASSES = True
    VAL_INTERVAL = 1
    WEIGHTS_SAVE_INTERVAL = 1
    WEIGHTS_INIT = 'weights/training/model_best.pkl'
    # WEIGHTS_INIT = '/home/ars/sda6/work/play/wk-classify/local/cigarette_defect/weights/trained/cigarette_box_defect/model_final_[acc=1].pkl'
    TRAIN_DIR = '/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1-train'
    VAL_DIR = '/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1-val'
    # VAL_DIR = '/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1'
    # VAL_DIR = '/home/ars/sda5/data/烟盒/datasets/dataset/val'
    val_transform = EasyTransform([
        t.Resize(INPUT_SIZE[::-1]),
        t.SaveToDir('data/test'),
        t.ToTensor(),
    ])
    train_transform = EasyTransform([
        t.ColorJitter(brightness=0.2, contrast=0, saturation=0, hue=0),
        # t.ColorJitter(brightness=0.2, contrast=0.1, saturation=0.1, hue=0.05),
        # t.RandomHorizontalFlip(),
        # t.RandomVerticalFlip(),
        # t.RandomRotate(360),
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
