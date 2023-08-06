from torchvision.models import resnet18, resnet34, resnet50, resnet101, resnet152, resnext50_32x4d, resnext101_32x8d, \
    wide_resnet101_2, wide_resnet50_2, alexnet, densenet121, densenet161, densenet169, densenet201, googlenet, \
    mnasnet0_5, mnasnet0_75, mnasnet1_0, mnasnet1_3, mobilenet_v2, inception_v3, shufflenet_v2_x0_5, shufflenet_v2_x1_0, \
    shufflenet_v2_x1_5, shufflenet_v2_x2_0


torchvision_models_dict = dict(
    resnet18=resnet18, resnet34=resnet34, resnet50=resnet50, resnet101=resnet101, resnet152=resnet152,
    resnext50_32x4d=resnext50_32x4d, resnext101_32x8d=resnext101_32x8d, wide_resnet101_2=wide_resnet101_2,
    wide_resnet50_2=wide_resnet50_2, alexnet=alexnet, densenet121=densenet121, densenet161=densenet161,
    densenet169=densenet169, densenet201=densenet201, googlenet=googlenet, mnasnet0_5=mnasnet0_5,
    mnasnet0_75=mnasnet0_75, mnasnet1_0=mnasnet1_0, mnasnet1_3=mnasnet1_3, mobilenet_v2=mobilenet_v2,
    inception_v3=inception_v3, shufflenet_v2_x0_5=shufflenet_v2_x0_5, shufflenet_v2_x1_0=shufflenet_v2_x1_0,
    shufflenet_v2_x1_5=shufflenet_v2_x1_5, shufflenet_v2_x2_0=shufflenet_v2_x2_0
)
