
import os, shutil, glob, random
from PIL import Image
import torch

IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')


def load_image_files(dir,recursive=False):
    fs=[]
    for ext in IMG_EXTENSIONS:
        if recursive:
            fs += glob.glob(dir + '/**/*' + ext,recursive=True)
        else:
            fs += glob.glob(dir + '/*' + ext)
    return fs
def load_image_folder(path):
    classes = os.listdir(path)
    files = {cls: [] for cls in classes}
    for cls in classes:
        cls_dir = os.path.join(path, cls)
        for ext in IMG_EXTENSIONS:
            files[cls] += glob.glob(cls_dir + '/*' + ext)
    return files

def adaptive_duplicate(class_files):
    max_length = max([len(fs) for fs in class_files.values()])
    new_class_files = {}
    for cls, fs in class_files.items():
        # new_class_files[cls] = fs + random.choices(fs, k=max_length - len(fs))
        scale=int(max_length//len(fs))
        new_class_files[cls] = fs*scale
        print(cls,scale)
    return new_class_files


class ImageFolder:
    def __init__(self, path, balance_classes=False, transform=None):
        self.class_files = load_image_folder(path)
        if balance_classes:
            self.class_files = adaptive_duplicate(self.class_files)
        for k,v in self.class_files.items():
            print(k,len(v))
        self.classes = sorted(list(self.class_files.keys()))
        self.cls2idx = {cls: i for i, cls in enumerate(self.classes)}
        self.data = []
        for cls, fs in self.class_files.items():
            self.data += list(zip(fs, [self.cls2idx[cls]] * len(fs)))
        self.transform = transform

    def __getitem__(self, item):
        img_path, cls_idx = self.data[item]
        img = Image.open(img_path)
        if self.transform:
            img = self.transform(img)
        return img, cls_idx

    def __len__(self):
        return len(self.data)


class Dataset:
    def __init__(self, path=None, balance_classes=False, transform=None, data=None, batch_size=16, device=None,
                 shuffle=True):
        data = data or ImageFolder(path, balance_classes, transform)
        self.data=data
        self.classes = data.classes
        self.num_classes = len(self.classes)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.index_list = list(range(len(data)))
        if shuffle:
            random.shuffle(self.index_list)
        self.num_batches = len(self.index_list) // self.batch_size
        self.current_batch_index = -1
        if not device:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.device = device
    def __len__(self):
        return self.num_batches
    def __iter__(self):
        return self

    def __next__(self):
        self.current_batch_index += 1
        if self.current_batch_index == self.num_batches:
            if self.shuffle:
                random.shuffle(self.index_list)
            self.current_batch_index = -1
            raise StopIteration
        batch_inds = self.index_list[
                     self.current_batch_index * self.batch_size:(self.current_batch_index + 1) * self.batch_size]
        batch_img = []
        batch_labels = []
        for ind in batch_inds:
            img, cls_idx = self.data[ind]
            img=torch.unsqueeze(img,0)
            batch_img.append(img)
            batch_labels.append(cls_idx)
        batch_img = torch.cat(batch_img, dim=0)
        batch_img = batch_img.to(self.device)
        batch_labels = torch.tensor(batch_labels).to(self.device)
        return batch_img, batch_labels


def demo():
    pass
