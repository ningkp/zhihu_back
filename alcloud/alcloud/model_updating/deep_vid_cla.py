import os
import pickle

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from torch.autograd import Variable
from torchvision.models.detection.faster_rcnn import FasterRCNN, resnet_fpn_backbone

from ..config import PRETRAINED_DEEP_MODEL_DIR, TRAINED_DEEP_MODEL_DIR
from ..feature.img_feature import load_model
from ..utils.data_manipulate import create_img_dataloader


class AlCloudPytorchVidClaModel:
    """C3D, R3D, R2+1D"""

    def __init__(self, project_id, model_name=None, num_classes=None, pytorch_model=None):
        self._proj_id = project_id

        if os.path.exists(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl')):
            with open(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl'), 'rb') as f:
                self.model_ft = pickle.load(f)
        elif pytorch_model:
            assert isinstance(
                pytorch_model, nn.Module), 'pytorch_model must inherit from torch.nn.Module'
            self.model_ft = pytorch_model
        else:
            assert model_name in MODEL_NAME.keys(
            ), 'model_name must be one of {}'.format(MODEL_NAME.keys())
            if not num_classes:
                raise ValueError(
                    "Deep model of project {} is not initialized, please specify the model name and number of classes.".format(
                        project_id))
            self._num_classes = num_classes

            # load model & modify the output shape
            self.model_ft = load_model(model_name)

    def fit(self, data_dir, label, transform=None,
            batch_size=20, clip_len=16, num_workers=4, 
            shuffle=False, data_names=None,
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

        :param batch_size: int, optional (default=20)
            Batch size when training.

        :param clip_len: int, optional (default=16)
            How many frames in a batch.

        :param num_workers: int, optional (default=4)
            Number of worker.

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
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        assert isinstance(label, dict)
        # dataloader = create_img_dataloader(data_dir=data_dir, labels=label, transform=transform,
        #                                    data_names=data_names, batch_size=batch_size, shuffle=shuffle)
        dataloader = DataLoader(VideoDataset(dataset=data_dir, split='train',
                                             clip_len=clip_len), batch_size=batch_size, 
                                             shuffle=shuffle, num_workers=num_workers)

        # prepare parameters to be updated
        params_to_update = [
            p for p in self.model_ft.parameters() if p.requires_grad]

        # Observe that all parameters are being optimized
        try:
            eval('from torch.optim import ' + optimize_method)
        except:
            ValueError("optimize_method must in ['Adadelta', 'Adagrad', 'Adam', 'SparseAdam', 'Adamax',\
                       'ASGD', 'SGD', 'Rprop', 'RMSprop', 'LBFGS']")
        if optimize_param:
            assert isinstance(optimize_param, dict)
            optimizer_ft = eval('optim.' + optimize_method +
                                "(params_to_update,  **optimize_param)")
        else:
            optimizer_ft = eval(
                'optim.' + optimize_method + "(params_to_update)")

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
            for inputs, labels in dataloader:
                # move inputs and labels to the device the training is taking place on
                inputs = Variable(inputs, requires_grad=True).to(device)
                labels = Variable(labels).to(device)
                optimizer_ft.zero_grad()

                outputs = self.model_ft(inputs)

                probs = nn.Softmax(dim=1)(outputs)
                preds = torch.max(probs, 1)[1]
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
            outputs = self.model_ft(inputs)
            result.append(outputs.flatten().detach().numpy())
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
        proba_result = self.predict_proba(
            data_dir=data_dir, data_names=data_names, transform=transform)
        return np.argmax(proba_result, axis=1)

    def save_model(self):
        # save model
        with open(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl'), 'wb') as f:
            pickle.dump(self.model_ft, f)
