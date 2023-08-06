import numpy as np
from torchvision import transforms
from wpcv.utils.data_aug import img_aug, random_float_generator
from wpcv.utils.ops import pil_ops

class EasyTransform(list):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.finalized=False
        self.trans=None
    def ColorJitter(self, brightness=0.1, contrast=0.05, saturation=0.05, hue=0.02):
        T = transforms.ColorJitter(brightness=brightness, contrast=contrast, saturation=contrast, hue=hue)
        self.append(T)
        return T

    def RandomHorizontalFlip(self, **kwargs):
        T = transforms.RandomHorizontalFlip(**kwargs)
        self.append(T)
        return T

    def RandomVerticalFlip(self, **kwargs):
        T = transforms.RandomVerticalFlip(**kwargs)
        self.append(T)
        return T

    def RandomRotate(self, degree):
        T = img_aug.RandomApply(pil_ops.rotate, random_params=dict(degree=random_float_generator(degree)))
        self.append(T)
        return T

    def RandomTranslate(self, offset):
        T = img_aug.RandomApply(pil_ops.translate,
                                random_params=dict(offset=random_float_generator(offset, shape=(2,),
                                                                                 dtype=np.int)))
        self.append(T)
        return T

    def RandomShear(self, degree1, degree2):
        T = img_aug.RandomApply(pil_ops.shear_xy,
                                random_params=dict(degree1=random_float_generator(degree1),
                                                   degree2=random_float_generator(degree2)))
        self.append(T)
        return T

    def RandomBlur(self, radius=1, p=0.3):
        T = img_aug.RandomApply(pil_ops.gaussian_blur, radius=radius, p=p)
        self.append(T)
        return T

    def RandomSPNoinse(self, p=0.3):
        T = img_aug.RandomApply(pil_ops.sp_noise, p=p)
        self.append(T)
        return T

    def Resize(self, size):
        T = transforms.Resize(size[::-1])
        self.append(T)
        return T

    def RandomApply(self, t, p, **kwargs):
        T = img_aug.RandomApply(t, p=p, **kwargs)
        self.append(T)
        return T

    def ToTensor(self):
        T = transforms.ToTensor()
        self.append(T)
        return T

    def Compose(self, trans):
        T = transforms.Compose(trans)
        self.append(T)
        return T
    def __call__(self, *args, **kwargs):
        if not  self.finalized:
            self.trans=self._final()
            self.finalized=True
        return self.trans(*args,**kwargs)
    def _final(self):
        return transforms.Compose(self)

t=EasyTransform()