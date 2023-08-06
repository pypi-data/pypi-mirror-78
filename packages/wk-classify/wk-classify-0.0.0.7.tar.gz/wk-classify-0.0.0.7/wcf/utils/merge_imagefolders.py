import wk
import wpcv
import os,shutil,glob

IMAGE_FIEL_EXT=['.jpg','.jpeg','.png','.bmp']

def get_image_paths(dir):
    fs=[]
    for ext in IMAGE_FIEL_EXT:
        fs+=glob.glob(dir+'/*'+ext)
    return fs
def merge(src_dirs,dst=None,overwrite=True):
    dst=dst or os
    wk.remake(dst)
    for dir in src_dirs:
        for cls in os.listdir(dir):
            cls_dir=os.path.join(dir,cls)
            dst_cls_dir=os.path.join(dst,cls)
            cls_fs=get_image_paths(cls_dir)
            wk.copy_files_to(cls_fs,dst_cls_dir,overwrite=overwrite)
            print(dir,cls)
    print('finished.')

if __name__ == '__main__':
    merge(
        src_dirs=[
            '/home/ars/sda5/data/电容/图片整理/work/Cam1/比较好分',
            '/home/ars/sda5/data/电容/图片整理/work/Cam1/比较好分2'
        ],
        dst='/home/ars/sda5/data/电容/图片整理/work/Cam1/合并'
    )



