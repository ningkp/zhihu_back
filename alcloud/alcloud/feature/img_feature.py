'''
Use a pre-trained deep model to extract the image feature
'''

import os
import pickle
import sys
import re

import numpy as np
import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from torchvision import models
import torch.utils.data as Data
# from ..config import PRETRAINED_DEEP_MODEL_DIR
from data_manipulate import create_img_dataloader

file_dir = os.path.dirname(__file__)
TEST_RES_DIR = os.path.join(os.path.dirname(file_dir), 'test_resource')
PRETRAINED_DEEP_MODEL_DIR = os.path.join(TEST_RES_DIR, 'pre_trained_models')
TRAINED_DEEP_MODEL_DIR = os.path.join(TEST_RES_DIR, 'trained_models')

MODEL_NAME = {'VGG': 'vgg19_bn.pth',
              'ResNet': 'resnet152.pth',
              'DenseNet': 'densenet201.pth',
              'AlexNet': 'alexnet.pth',
              'GoogleNet': 'googlenet.pth',
              'ResNext101': 'resnext101.pth',
              }

__all__ = ['extract_cnn',
           'load_model'
           ]

######################################################################
# Initialize and Reshape the Networks
# -----------------------------------
#
# Now to the most interesting part. Here is where we handle the reshaping
# of each network. Note, this is not an automatic procedure and is unique
# to each model. Recall, the final layer of a CNN model, which is often
# times an FC layer, has the same number of nodes as the number of output
# classes in the dataset. Since all of the models have been pretrained on
# Imagenet, they all have output layers of size 1000, one node for each
# class. The goal here is to reshape the last layer to have the same
# number of inputs as before, AND to have the same number of outputs as
# the number of classes in the dataset. In the following sections we will
# discuss how to alter the architecture of each model individually. But
# first, there is one important detail regarding the difference between
# finetuning and feature-extraction.
#
# When feature extracting, we only want to update the parameters of the
# last layer, or in other words, we only want to update the parameters for
# the layer(s) we are reshaping. Therefore, we do not need to compute the
# gradients of the parameters that we are not changing, so for efficiency
# we set the .requires_grad attribute to False. This is important because
# by default, this attribute is set to True. Then, when we initialize the
# new layer and by default the new parameters have ``.requires_grad=True``
# so only the new layer’s parameters will be updated. When we are
# finetuning we can leave all of the .required_grad’s set to the default
# of True.
#
# Finally, notice that inception_v3 requires the input size to be
# (299,299), whereas all of the other models expect (224,224).
#
# Resnet
# ~~~~~~
#
# Resnet was introduced in the paper `Deep Residual Learning for Image
# Recognition <https://arxiv.org/abs/1512.03385>`__. There are several
# variants of different sizes, including Resnet18, Resnet34, Resnet50,
# Resnet101, and Resnet152, all of which are available from torchvision
# models. Here we use Resnet18, as our dataset is small and only has two
# classes. When we print the model, we see that the last layer is a fully
# connected layer as shown below:
#
# ::
#
#    (fc): Linear(in_features=512, out_features=1000, bias=True)
#
# Thus, we must reinitialize ``model.fc`` to be a Linear layer with 512
# input features and 2 output features with:
#
# ::
#
#    model.fc = nn.Linear(512, num_classes)
#
# Alexnet
# ~~~~~~~
#
# Alexnet was introduced in the paper `ImageNet Classification with Deep
# Convolutional Neural
# Networks <https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf>`__
# and was the first very successful CNN on the ImageNet dataset. When we
# print the model architecture, we see the model output comes from the 6th
# layer of the classifier
#
# ::
#
#    (classifier): Sequential(
#        ...
#        (6): Linear(in_features=4096, out_features=1000, bias=True)
#     )
#
# To use the model with our dataset we reinitialize this layer as
#
# ::
#
#    model.classifier[6] = nn.Linear(4096,num_classes)
#
# VGG
# ~~~
#
# VGG was introduced in the paper `Very Deep Convolutional Networks for
# Large-Scale Image Recognition <https://arxiv.org/pdf/1409.1556.pdf>`__.
# Torchvision offers eight versions of VGG with various lengths and some
# that have batch normalizations layers. Here we use VGG-11 with batch
# normalization. The output layer is similar to Alexnet, i.e.
#
# ::
#
#    (classifier): Sequential(
#        ...
#        (6): Linear(in_features=4096, out_features=1000, bias=True)
#     )
#
# Therefore, we use the same technique to modify the output layer
#
# ::
#
#    model.classifier[6] = nn.Linear(4096,num_classes)
#
# Squeezenet
# ~~~~~~~~~~
#
# The Squeeznet architecture is described in the paper `SqueezeNet:
# AlexNet-level accuracy with 50x fewer parameters and <0.5MB model
# size <https://arxiv.org/abs/1602.07360>`__ and uses a different output
# structure than any of the other models shown here. Torchvision has two
# versions of Squeezenet, we use version 1.0. The output comes from a 1x1
# convolutional layer which is the 1st layer of the classifier:
#
# ::
#
#    (classifier): Sequential(
#        (0): Dropout(p=0.5)
#        (1): Conv2d(512, 1000, kernel_size=(1, 1), stride=(1, 1))
#        (2): ReLU(inplace)
#        (3): AvgPool2d(kernel_size=13, stride=1, padding=0)
#     )
#
# To modify the network, we reinitialize the Conv2d layer to have an
# output feature map of depth 2 as
#
# ::
#
#    model.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1,1), stride=(1,1))
#
# Densenet
# ~~~~~~~~
#
# Densenet was introduced in the paper `Densely Connected Convolutional
# Networks <https://arxiv.org/abs/1608.06993>`__. Torchvision has four
# variants of Densenet but here we only use Densenet-121. The output layer
# is a linear layer with 1024 input features:
#
# ::
#
#    (classifier): Linear(in_features=1024, out_features=1000, bias=True)
#
# To reshape the network, we reinitialize the classifier’s linear layer as
#
# ::
#
#    model.classifier = nn.Linear(1024, num_classes)
#
# Inception v3
# ~~~~~~~~~~~~
#
# Finally, Inception v3 was first described in `Rethinking the Inception
# Architecture for Computer
# Vision <https://arxiv.org/pdf/1512.00567v1.pdf>`__. This network is
# unique because it has two output layers when training. The second output
# is known as an auxiliary output and is contained in the AuxLogits part
# of the network. The primary output is a linear layer at the end of the
# network. Note, when testing we only consider the primary output. The
# auxiliary output and primary output of the loaded model are printed as:
#
# ::
#
#    (AuxLogits): InceptionAux(
#        ...
#        (fc): Linear(in_features=768, out_features=1000, bias=True)
#     )
#     ...
#    (fc): Linear(in_features=2048, out_features=1000, bias=True)
#
# To finetune this model we must reshape both layers. This is accomplished
# with the following
#
# ::
#
#    model.AuxLogits.fc = nn.Linear(768, num_classes)
#    model.fc = nn.Linear(2048, num_classes)
#
# Notice, many of the models have similar output structures, but each must
# be handled slightly differently. Also, check out the printed model
# architecture of the reshaped network and make sure the number of output
# features is the same as the number of classes in the dataset.
#

def conv3x3(in_planes, out_planes, stride=1):
    """3x3 convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                     padding=1, bias=False)


def conv1x1(in_planes, out_planes, stride=1):
    """1x1 convolution"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


class _Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(_Bottleneck, self).__init__()
        self.conv1 = conv1x1(inplanes, planes)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = conv3x3(planes, planes, stride)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = conv1x1(planes, planes * self.expansion)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


_vgg_cfg = {
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}

model_urls = {
    # Inception v3 ported from TensorFlow
    'inception_v3_google': 'https://download.pytorch.org/models/inception_v3_google-1a9a5a14.pth',
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
    'vgg11': 'https://download.pytorch.org/models/vgg11-bbd30ac9.pth',
    'vgg13': 'https://download.pytorch.org/models/vgg13-c768596a.pth',
    'vgg16': 'https://download.pytorch.org/models/vgg16-397923af.pth',
    'vgg19': 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth',
    'vgg11_bn': 'https://download.pytorch.org/models/vgg11_bn-6002323d.pth',
    'vgg13_bn': 'https://download.pytorch.org/models/vgg13_bn-abd245e5.pth',
    'vgg16_bn': 'https://download.pytorch.org/models/vgg16_bn-6c64b313.pth',
    'vgg19_bn': 'https://download.pytorch.org/models/vgg19_bn-c79401a0.pth',
    'alexnet': 'https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth',
    'densenet121': 'https://download.pytorch.org/models/densenet121-a639ec97.pth',
    'densenet169': 'https://download.pytorch.org/models/densenet169-b2777c0a.pth',
    'densenet201': 'https://download.pytorch.org/models/densenet201-c1103571.pth',
    'densenet161': 'https://download.pytorch.org/models/densenet161-8d451a50.pth',
    'squeezenet1_0': 'https://download.pytorch.org/models/squeezenet1_0-a815701f.pth',
    'squeezenet1_1': 'https://download.pytorch.org/models/squeezenet1_1-f364aa15.pth',
    'googlenet': 'https://download.pytorch.org/models/googlenet-1378be20.pth',
    'resnext101_32x8d': 'https://download.pytorch.org/models/resnext101_32x8d-8ba56ff5.pth',
}


def _vgg_make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


def download_model(saving_path='.'):
    # inception net
    # model = models.Inception3()
    # model.load_state_dict(model_zoo.load_url(model_urls['inception_v3_google'], model_dir=saving_path, progress=True))

    # resnet
    model = models.ResNet(_Bottleneck, [3, 8, 36, 3])
    model.load_state_dict(model_zoo.load_url(model_urls['resnet152'], model_dir=saving_path, progress=True))
    # save_model(model, 'resnet152.pkl', saving_path)

    # alex net
    model = models.AlexNet()
    model.load_state_dict(model_zoo.load_url(model_urls['alexnet'], model_dir=saving_path, progress=True))
    # save_model(model, 'alexnet.pkl', saving_path)

    # vgg
    model = models.VGG(_vgg_make_layers(_vgg_cfg['E'], batch_norm=True), init_weights=False)
    model.load_state_dict(model_zoo.load_url(model_urls['vgg19_bn'], model_dir=saving_path, progress=True))
    # save_model(model, 'vgg19.pkl', saving_path)

    # squeeze net
    model = models.SqueezeNet(version=1.1)
    model.load_state_dict(model_zoo.load_url(model_urls['squeezenet1_1'], model_dir=saving_path, progress=True))
    # save_model(model, 'squeezenet1_1.pkl', saving_path)

    # dense net
    model = models.DenseNet(num_init_features=64, growth_rate=32, block_config=(6, 12, 48, 32))
    pattern = re.compile(
        r'^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$')
    state_dict = model_zoo.load_url(model_urls['densenet201'], model_dir=saving_path, progress=True)
    for key in list(state_dict.keys()):
        res = pattern.match(key)
        if res:
            new_key = res.group(1) + res.group(2)
            state_dict[new_key] = state_dict[key]
            del state_dict[key]
    model.load_state_dict(state_dict)
    # save_model(model, 'densenet201.pkl', saving_path)

    # googlenet
    kwargs = dict()
    kwargs['transform_input'] = True
    kwargs['aux_logits'] = False
    # if kwargs['aux_logits']:
    #     warnings.warn('auxiliary heads in the pretrained googlenet model are NOT pretrained, '
    #                   'so make sure to train them')
    original_aux_logits = kwargs['aux_logits']
    kwargs['aux_logits'] = True
    kwargs['init_weights'] = False
    model = models.GoogLeNet(**kwargs)
    model.load_state_dict(model_zoo.load_url(model_urls['googlenet']))
    if not original_aux_logits:
        model.aux_logits = False
        del model.aux1, model.aux2
        # save_model(model, 'googlenet.pkl', saving_path)

    # resnext
    model = models.resnext101_32x8d(pretrained=False)
    model.load_state_dict(model_zoo.load_url(model_urls['resnext101_32x8d'], model_dir=saving_path, progress=True))


def save_model(model_object, file_name, saving_path='.'):
    with open(os.path.join(saving_path, file_name), 'wb') as f:
        pickle.dump(model_object, f)


def load_model(model_name):
    global MODEL_NAME
    # Detect if we have a GPU available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if model_name == 'ResNet':
        model = models.resnet152(pretrained=False)
        model.load_state_dict(torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME[model_name]), map_location=device))
    elif model_name == 'AlexNet':
        model = models.AlexNet()
        model.load_state_dict(torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME[model_name]), map_location=device))
    elif model_name == 'VGG':
        model = models.VGG(_vgg_make_layers(_vgg_cfg['E'], batch_norm=True), init_weights=False)
        model.load_state_dict(torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME[model_name]), map_location=device))
    elif model_name == 'DenseNet':
        model = models.DenseNet(num_init_features=64, growth_rate=32, block_config=(6, 12, 48, 32))
        pattern = re.compile(
            r'^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$')
        state_dict = torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME[model_name]), map_location=device)
        for key in list(state_dict.keys()):
            res = pattern.match(key)
            if res:
                new_key = res.group(1) + res.group(2)
                state_dict[new_key] = state_dict[key]
                del state_dict[key]
        model.load_state_dict(state_dict)
    elif model_name == 'GoogleNet':
        # googlenet
        kwargs = dict()
        kwargs['transform_input'] = True
        kwargs['aux_logits'] = False
        # if kwargs['aux_logits']:
        #     warnings.warn('auxiliary heads in the pretrained googlenet model are NOT pretrained, '
        #                   'so make sure to train them')
        original_aux_logits = kwargs['aux_logits']
        kwargs['aux_logits'] = True
        kwargs['init_weights'] = False
        model = models.GoogLeNet(**kwargs)
        model.load_state_dict(torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME[model_name]), map_location=device))
        if not original_aux_logits:
            model.aux_logits = False
            del model.aux1, model.aux2
    elif model_name == 'ResNext101':
        model = models.resnext101_32x8d(pretrained=False)
        model.load_state_dict(torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME[model_name]), map_location=device))
    else:
        raise ValueError("Model name must be one of ['VGG', 'ResNet', 'DenseNet', 'AlexNet', 'GoogleNet', 'ResNext101']")

    model.eval()
    return model


class DenseExtractor(nn.Module):
    def __init__(self, dense_obj):
        super(DenseExtractor, self).__init__()
        self.features = dense_obj.features

    def forward(self, x):
        features = self.features(x)
        out = torch.nn.functional.relu(features, inplace=True)
        out = torch.nn.functional.adaptive_avg_pool2d(out, (1, 1)).view(features.size(0), -1)
        return out


class AlexExtractor(nn.Module):
    def __init__(self, alex_obj):
        super(AlexExtractor, self).__init__()
        self.features = alex_obj.features
        self.avgpool = alex_obj.avgpool
        self.classifier = nn.Sequential(*list(alex_obj.classifier.children())[:-1])

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), 256 * 6 * 6)
        x = self.classifier(x)
        return x


class VGGExtractor(nn.Module):
    def __init__(self, vgg_obj):
        super(VGGExtractor, self).__init__()
        self.features = vgg_obj.features
        self.avgpool = vgg_obj.avgpool
        self.classifier = nn.Sequential(*list(vgg_obj.classifier.children())[:-1])

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def extract_cnn(dataset, model_name):
    """Extract a 2D feature matrix for the given dataset.

    :param dataset: torch.utils.data.DataLoader
        Dataloader object in pytorch.

    :param model_name: str
        MODEL_NAME = {'VGG': 'vgg19_bn.pth',
              'ResNet': 'resnet152.pth',
              'DenseNet': 'densenet201.pth',
              'AlexNet': 'alexnet.pth',
              'GoogleNet': 'googlenet.pth',
              'ResNext101': 'resnext101.pth',
              }
    """
    features = load_model(model_name=model_name)
    # remove the classification layer
    # Note: this doesn't work with inception-v3 model
    if model_name == 'DenseNet':
        features = DenseExtractor(features)
    elif model_name == 'AlexNet':
        features = AlexExtractor(features)
    elif model_name == 'VGG':
        features = VGGExtractor(features)
    else:
        features = nn.Sequential(*list(features.children())[:-1])
    # print(model)
    # print(features)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    features = features.to(device)
    features.eval()

    feature_2d = []
    feature_name = []
    for batch in dataset:
        inputs = batch['image'].to(device)
        ext_fea = features(inputs)
        # print(ext_fea.shape)
        print(ext_fea.flatten().cpu().detach().numpy())
        #
        # print(len(ext_fea.flatten().detach().numpy()))
        # print(batch['image_name'])
        feature_2d.append(ext_fea.flatten().cpu().detach().numpy())
        feature_name.append(batch['image_name'])

        # for testing
        # print(model.features(inputs) == features.features(inputs))

    return np.asarray(feature_2d), feature_name

if __name__ == '__main__':
    dataSet = sys.argv[1]
    modelName = sys.argv[2]
    saveFile = sys.argv[3]
    modelName = 'VGG'

    TEST_DATA_DIR = dataSet
    img_dataset = create_img_dataloader(TEST_DATA_DIR)
    with torch.no_grad():
        feature_mat, data_name = extract_cnn(img_dataset, model_name=modelName)     # 1024 dim

    with open(saveFile,'wb') as f:
        temp = {"fea_vector":feature_mat,"data_name":data_name}
        pickle.dump(temp,f)

    #写入文件
    print(feature_mat)
