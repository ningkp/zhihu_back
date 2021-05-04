import os
from img_feature import extract_cnn
from config import TEST_RES_DIR
from data_manipulate import create_img_dataloader

MODEL_NAME = {'VGG': 'vgg19_bn.pth',
              'ResNet': 'resnet152.pth',
              'DenseNet': 'densenet201.pth',
              'AlexNet': 'alexnet.pth',
              'GoogleNet': 'googlenet.pth',
              'ResNext101': 'resnext101.pth',
              }
# TEST_DATA_DIR = '/home/ying-peng/Code/alcloud/test_resource/images'
TEST_DATA_DIR = os.path.join(TEST_RES_DIR, 'images')

img_dataset = create_img_dataloader(TEST_DATA_DIR)

# feature_mat, data_name = extract_cnn(img_dataset, model_name='GoogleNet')     # 1024 dim
# print('GoogleNet:\t', feature_mat.shape, data_name)
# feature_mat, data_name = extract_cnn(img_dataset, model_name='DenseNet')      # 1920 dim
# print('DenseNet:\t', feature_mat.shape, data_name)
# feature_mat, data_name = extract_cnn(img_dataset, model_name='ResNet')        # 2048 dim
# print('ResNet:\t', feature_mat.shape, data_name)
# feature_mat, data_name = extract_cnn(img_dataset, model_name='AlexNet')       # 4096 dim
# print('AlexNet:\t', feature_mat.shape, data_name)
feature_mat, data_name = extract_cnn(img_dataset, model_name='VGG')           # 4096 dim
print('VGG:\t', feature_mat.shape, data_name)
# feature_mat, data_name = extract_cnn(img_dataset, model_name='ResNext101')           # 2048 dim
# print('ResNext101:\t', feature_mat.shape, data_name)
