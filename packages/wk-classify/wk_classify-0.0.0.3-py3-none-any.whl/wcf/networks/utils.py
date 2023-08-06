from .ptcv_models import ptcv_models_dict
from torch import nn
from .torchvision_models import torchvision_models_dict



def load_model(model_type,num_classes,pretrained=False):
    if callable(model_type):
        return model_type(pretrained=pretrained,num_classes=num_classes)
    if model_type in torchvision_models_dict.keys():
        model=torchvision_models_dict[model_type](pretrained=pretrained)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
    elif model_type in ptcv_models_dict.keys():
        model=ptcv_models_dict[model_type](pretrained=pretrained)
        model.features.final_pool=nn.AdaptiveAvgPool2d((1, 1))
        if isinstance(model.output,nn.Linear):
            model.output=nn.Linear(model.output.in_features, num_classes)
        else:
            model.output.fc = nn.Linear(model.output.fc.in_features, num_classes)
    else:
        raise Exception('Model %s not found.'%(model_type))
    return model

