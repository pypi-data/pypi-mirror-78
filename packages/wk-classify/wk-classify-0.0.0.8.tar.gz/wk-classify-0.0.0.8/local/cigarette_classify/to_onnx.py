import torch
from wcf.networks import load_model
from torchvision import transforms
import numpy as np
import cv2
import os,glob,shutil
from PIL import Image
import onnxruntime

def get_model():
    return load_model('shufflenet_v2_x0_5',17)
    # return load_model('resnet18',17)
def to_onnx(model_path, out_path='model.onnx'):
    w,h=284,252
    dummy_input = torch.randn(1, 3, h, w, device='cpu')
    match_dict = torch.load(model_path)
    model = get_model()
    model.load_state_dict(match_dict)
    model.eval()
    input_names = ["input"]
    output_names = ["output"]
    torch.onnx.export(model, dummy_input, out_path, verbose=True, input_names=input_names,
                      output_names=output_names)


def load_onnx_model(model_path):
    ort_session = onnxruntime.InferenceSession(model_path)
    return ort_session
def inference_onnx(ort_session,img):
    ort_inputs = {ort_session.get_inputs()[0].name: img}
    ort_outs = ort_session.run(None, ort_inputs)
    return ort_outs



def test_onnx():

    model=load_onnx_model('model.onnx')
    classes=open('classes.txt').read().strip().split('\n')
    dir='/home/ars/sda5/data/projects/烟分类/data/烟分类-val'
    ext='.bmp'
    fs=glob.glob(dir+"/**/*"+ext,recursive=True)
    for i,f in enumerate(fs):
        img = cv2.imread(f)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (284, 252))
        img = np.array(img, dtype=np.float).astype(np.float32)/255
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, 0)
        outputs = inference_onnx(model, img)[0]
        print(outputs)
        outputs = torch.softmax(torch.from_numpy(outputs), dim=1)
        prob, cls = torch.max(outputs, dim=1)
        print(prob,cls)
        cls = int(cls.item())
        prob = float(prob.item())
        cls=classes[cls]
        print(f,cls,prob)

def test():
    model_path='weights/training/model_best.pkl'
    test_dir='/home/ars/sda5/data/projects/烟分类/data/烟分类-val'
    # classes=['NG','OK']
    classes=open('classes.txt').read().strip().split('\n')
    input_size=(284,252)
    device = torch.device('cpu')
    model=get_model()
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    model.eval()
    transform =  transforms.Compose([
        transforms.Resize(input_size[::-1]),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    ext='.bmp'
    fs=glob.glob(test_dir+"/**/*"+ext,recursive=True)
    for i,f in enumerate(fs):
    # for i,f in enumerate(10):
        img=Image.open(f)
        img=transform(img).float()
        img=torch.tensor(img).unsqueeze(0).to(device)

        outputs=model(img)
        outputs = torch.softmax(outputs, dim=1)
        probs, preds = torch.max(outputs, dim=1)
        pred = int(preds[0])
        prob = float(probs[0])
        cls=classes[pred]

        print(i,f,cls,prob)

if __name__ == '__main__':
    # to_onnx('weights/training/model_best.pkl')
    test_onnx()
    # test()