from wcf.utils.split_trainval import split_train_val_imagefolder

split_train_val_imagefolder(
    data_dir='/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1',
    train_dir='/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1-train',
    val_dir='/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1-val',
    val_split=0.3,
    ext='.bmp'
)