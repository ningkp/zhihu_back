import os
import pickle

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from torch.autograd import Variable
from ..config import TRAINED_DEEP_MODEL_DIR
from ..feature.img_feature import load_model
from ..utils.data_manipulate import create_img_dataloader

MODEL_NAME = {'VGG': 'vgg19_bn.pth',
              'ResNet': 'resnet152.pth',
              'DenseNet': 'densenet201.pth',
              'AlexNet': 'alexnet.pth',
              'GoogleNet': 'googlenet.pth',
              'ResNext101': 'resnext101.pth',
              }

__all__ = ['AlCloudPytorchImgClaModel',
           ]


class AlCloudPytorchImgClaModel:
    '''
    re-encapsulate pytorch model. {'VGG', 'ResNet', 'DenseNet', 'AlexNet', 'GoogleNet'}

    :param project_id: str
        The project id.

    :param model_name: str, optional
        The name of the target cnn.

    :param num_classes: int, optional
        The number of classes.

    :param pytorch_model: nn.Module, optional
        The customized pytorch model
    '''

    def __init__(self, project_id, model_name=None, num_classes=None, pytorch_model=None):
        self._proj_id = project_id

        if os.path.exists(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl')):
            with open(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl'), 'rb') as f:
                self.model_ft = pickle.load(f)
        elif pytorch_model:
            assert isinstance(pytorch_model, nn.Module), 'pytorch_model must inherit from torch.nn.Module'
            self.model_ft = pytorch_model
        else:
            assert model_name in MODEL_NAME.keys(), 'model_name must be one of {}'.format(MODEL_NAME.keys())
            if not num_classes:
                raise ValueError(
                    "Deep model of project {} is not initialized, please specify the model name and number of classes.".format(
                        project_id))
            self._num_classes = num_classes

            # load model & modify the output shape
            self.model_ft = load_model(model_name)
            # print(self.model_ft)
            if model_name == "GoogleNet" or model_name == "ResNet" or model_name == "ResNext101":
                num_ftrs = self.model_ft.fc.in_features
                self.model_ft.fc = nn.Linear(num_ftrs, num_classes)
            elif model_name == "AlexNet" or model_name == "VGG":
                num_ftrs = self.model_ft.classifier[6].in_features
                self.model_ft.classifier[6] = nn.Linear(num_ftrs, num_classes)
            elif model_name == "DenseNet":
                num_ftrs = self.model_ft.classifier.in_features
                self.model_ft.classifier = nn.Linear(num_ftrs, num_classes)
            # print(self.model_ft)


        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_ft = self.model_ft.to(self.device)

    def fit(self, data_dir, label, transform=None,
            batch_size=1, shuffle=False, data_names=None,
            optimize_method='Adam', optimize_param=None,
            loss='CrossEntropyLoss', loss_params=None, num_epochs=10, save_model=True):
        '''Fine tune the model.

        :param data_dir: str
            The path to the data folder.

        :param label: dict
            The labels of labeled set.
            Key: file name
            value: label

        :param transform: torchvision.transforms.Compose, optional (default=None)
            Transforms object that will be applied to the image data.

        :param batch_size: int, optional (default=1)
            Batch size when training.

        :param shuffle: bool, optional (default=False)
            Whether shuffle the data.

        :param data_names: list, optional (default=None)
            The data names. If not specified, it will all the files in the
            data_dir.

        :param optimize_method: str, optional (default='Adam')
            The optimization method. Should be one of
            ['Adadelta', 'Adagrad', 'Adam', 'SparseAdam', 'Adamax',
            'ASGD', 'SGD', 'Rprop', 'RMSprop', 'LBFGS']

        :param optimize_param: dict, optional (default=None)
            The keyword arguments which will be used for initializing the optimizer object.

        :param loss: str, optional (default='CrossEntropyLoss')
            Loss function. Should be one of
            ['L1Loss', 'NLLLoss', 'KLDivLoss', 'MSELoss', 'BCELoss', 'BCEWithLogitsLoss', 'NLLLoss2d',
            'CosineEmbeddingLoss', 'CTCLoss', 'HingeEmbeddingLoss', 'MarginRankingLoss',
            'MultiLabelMarginLoss', 'MultiLabelSoftMarginLoss', 'MultiMarginLoss',
            'SmoothL1Loss', 'SoftMarginLoss', 'CrossEntropyLoss', 'TripletMarginLoss', 'PoissonNLLLoss'].

        :param loss_params: dict, optional (default=None)
            The keyword arguments which will be used for initializing the loss object.

        :param num_epochs: int, optional (default=10)
            Number of epoch when training the model.

        :param save_model: bool, optional (default=True)
            Whether to save the model after training
        '''
        self.model_ft.train()
        assert isinstance(label, dict)
        dataloader = create_img_dataloader(data_dir=data_dir, labels=label, transform=transform,
                                           data_names=data_names, batch_size=batch_size, shuffle=shuffle)

        # prepare parameters to be updated
        params_to_update = [p for p in self.model_ft.parameters() if p.requires_grad]

        # Observe that all parameters are being optimized
        try:
            eval('from torch.optim import ' + optimize_method)
        except:
            ValueError("optimize_method must in ['Adadelta', 'Adagrad', 'Adam', 'SparseAdam', 'Adamax',\
                       'ASGD', 'SGD', 'Rprop', 'RMSprop', 'LBFGS']")
        if optimize_param:
            assert isinstance(optimize_param, dict)
            optimizer_ft = eval('optim.' + optimize_method + "(params_to_update,  **optimize_param)")
        else:
            optimizer_ft = eval('optim.' + optimize_method + "(params_to_update)")

        # Setup the loss fxn
        try:
            eval('from nn.modules.loss import ' + optimize_method)
        except:
            ValueError("loss must in ['L1Loss', 'NLLLoss', 'KLDivLoss', 'MSELoss', 'BCELoss', "
                       "'BCEWithLogitsLoss', 'NLLLoss2d','CosineEmbeddingLoss', 'CTCLoss', "
                       "'HingeEmbeddingLoss', 'MarginRankingLoss','MultiLabelMarginLoss', "
                       "'MultiLabelSoftMarginLoss', 'MultiMarginLoss', 'SmoothL1Loss', "
                       "'SoftMarginLoss', 'CrossEntropyLoss', 'TripletMarginLoss', 'PoissonNLLLoss']")

        if loss_params:
            assert isinstance(optimize_param, dict)
            criterion = eval('nn.' + loss + '(**loss_params)')
        else:
            criterion = eval('nn.' + loss + '()')

        for epoch in range(num_epochs):
            for batch in dataloader:
                inputs = batch['image']
                inputs_name = batch['image_name']
                labels = batch['target']

                inputs = inputs.to(self.device)
                labels = labels.to(self.device)

                # zero the parameter gradients
                optimizer_ft.zero_grad()
                # input should be (batch_size, channels, height, width)
                outputs = self.model_ft(inputs)

                # The labels is the label value (e.g., 3), not a list [0, 0, 0, 1]
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer_ft.step()

        if save_model:
            self.save_model()

    def predict_proba(self, data_dir, data_names=None, transform=None):
        '''proba predict.

        :param data_dir: str
            The path to the data folder.

        :param data_names: list, optional (default=None)
            The data names. If not specified, it will all the files in the
            data_dir.

        :param transform: torchvision.transforms.Compose, optional (default=None)
            Transforms object that will be applied to the image data.

        :return: pred: 2D array
            The proba prediction result. Shape [n_samples, n_classes]
        '''
        self.model_ft.eval()
        dataloader = create_img_dataloader(data_dir=data_dir, labels=None, transform=transform,
                                           batch_size=1, shuffle=False, data_names=data_names)
        result = []
        for batch in dataloader:
            inputs = batch['image']
            inputs = inputs.to(self.device)
            outputs = self.model_ft(inputs)
            result.append(outputs.cpu().flatten().detach().numpy())
        return np.asarray(result)

    def predict(self, data_dir, data_names=None, transform=None):
        '''predict

        :param data_dir: str
            The path to the data folder.

        :param data_names: list, optional (default=None)
            The data names. If not specified, it will all the files in the
            data_dir.

        :param transform: torchvision.transforms.Compose, optional (default=None)
            Transforms object that will be applied to the image data.

        :return: pred: 1D array
            The prediction result. Shape [n_samples]
        '''
        self.model_ft.eval()
        proba_result = self.predict_proba(data_dir=data_dir, data_names=data_names, transform=transform)
        return np.argmax(proba_result, axis=1)

    def save_model(self):
        # save model
        with open(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl'), 'wb') as f:
            pickle.dump(self.model_ft, f)


