from wcf.networks import load_model
from wk import Timer
model=load_model('shufflenet_v2_x0_5',num_classes=17)

import torch
device=torch.device('cpu')

model.eval()
model.to(device)
T=Timer()
img=torch.randn((1,3,210,350)).to((device))
for i in range(100):
    model(img)
    T.step()
print(T.mean())