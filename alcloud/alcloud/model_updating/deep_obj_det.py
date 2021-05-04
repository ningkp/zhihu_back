import os
import pickle
import subprocess

import torch
import torch.nn as nn
import torch.optim as optim

from torch.autograd import Variable
from torchvision import models
from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.backbone_utils import BackboneWithFPN
from torchvision.ops import misc as misc_nn_ops

from ..config import PRETRAINED_DEEP_MODEL_DIR, TRAINED_DEEP_MODEL_DIR, file_dir
from ..utils.data_manipulate import create_img_dataloader, create_faster_rcnn_dataloader
from ..third_party.yolov3.utils.datasets import ImgObjDetDataset, ImageFolder
from ..third_party.yolov3.utils.utils import non_max_suppression
from ..utils.detection.engine import train_one_epoch

MODEL_NAME = {'Faster_RCNN': 'fasterrcnn_resnet50_fpn_coco.pth',
              'Yolov3': 'resnet152.pth',
              }

__all__ = ['AlCloudPytorchObjDetModel',
           ]

"""
Pytorch official faster rcnn dataset requirement:

label_dict: dict
    key: file name
    value: list [[label_idx x0 y0 x1 y1], ...]
    
the dataset __getitem__ of object detection should return:

    image: a PIL Image of size (H, W)
    target: a dict containing the following fields
        boxes (FloatTensor[N, 4]): the coordinates of the N bounding boxes in [x0, y0, x1, y1] format, ranging from 0 to W and 0 to H
        labels (Int64Tensor[N]): the label for each bounding box
        image_id (Int64Tensor[1]): an image identifier. It should be unique between all the images in the dataset, and is used during evaluation
        area (Tensor[N]): The area of the bounding box. This is used during evaluation with the COCO metric, to separate the metric scores between small, medium and large boxes.
        iscrowd (UInt8Tensor[N]): instances with iscrowd=True will be ignored during evaluation.
        (optionally) masks (UInt8Tensor[N, H, W]): The segmentation masks for each one of the objects
        (optionally) keypoints (FloatTensor[N, K, 3]): For each one of the N objects, it contains the K keypoints in [x, y, visibility] format, defining the object. visibility=0 means that the keypoint is not visible. Note that for data augmentation, the notion of flipping a keypoint is dependent on the data representation, and you should probably adapt references/detection/transforms.py for your new keypoint representation


YOLOv3 dataset requirements:

ImgObjDetDataset(img_dir, label_dict)
label_dict: dict
    key: file name
    value: list [[label_idx x_center y_center width height], ...]
"""


class AlCloudPytorchObjDetModel:
    """Faster_RCNN, YOLOv3"""

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
            if model_name == 'Faster_RCNN':
                self.model_ft = _init_faster_rcnn(num_classes=num_classes)
            else:
                self.model_ft = _init_yolov3(num_classes=num_classes)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_ft = self.model_ft.to(self.device)

    def fit(self, data_dir, label, transform=None,
            batch_size=1, shuffle=False, data_names=None,
            optimize_method='Adam', optimize_param=None,
            loss='CrossEntropyLoss', loss_params=None, num_epochs=10,
            model_type='Faster_RCNN', save_model=True, **kwargs):
        '''Fine tune the model.

        :param data_dir: str
            The path to the data folder.

        :param label: dict
            The labels of labeled set.
            Key: file name
            value: a dict containing the following fields
            yolov3: [[label_idx x_center y_center width height], ...]
            rcnn: [[label_idx x0 y0 x1 y1], ...]

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

        :param num_epochs: {'Yolov3', 'Faster_RCNN'}, optional (default='Yolov3')
            model type.

        :param save_model: bool, optional (default=True)
            Whether to save the model after training

        :param **kwargs: dict, optional
            Parameters used to init yolo dataset object.
        '''
        self.model_ft.train()
        assert isinstance(label, dict)
        if model_type == 'Yolov3':
            dataloader = ImgObjDetDataset(img_dir=data_dir, label_dict=label, **kwargs)
            dataloader = torch.utils.data.DataLoader(
                dataloader,
                batch_size=batch_size,
                shuffle=True,
                num_workers=kwargs.pop('n_cpu', 0),
                pin_memory=True,
                collate_fn=dataloader.collate_fn,
            )
        else:
            dataloader = create_faster_rcnn_dataloader(data_dir=data_dir, label_dict=label, transform=transform,
                                                       augment=True, data_names=data_names, batch_size=batch_size,
                                                       shuffle=shuffle)

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

        # train
        for epoch in range(num_epochs):
            if model_type == 'Yolov3':
                # Be careful, input of yolov3 is strange.
                # See example training codes of yolov3
                # The labels is a list with len == 6,
                # the first element is 0, the others are label_idx x_center y_center width height

                # batch[0]: img_paths   batch[1]: input_imgs
                for batch in dataloader:
                    inputs = batch[1]
                    labels = batch[2]

                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)

                    loss, outputs = self.model_ft(inputs, labels)
                    loss.backward()

                    optimizer_ft.step()
                    optimizer_ft.zero_grad()

            else:
                # faster rcnn
                """
                During training, the model expects both the input tensors, as well as a targets dictionary,
                containing:
                    - boxes (Tensor[N, 4]): the ground-truth boxes in [x0, y0, x1, y1] format, with values
                      between 0 and H and 0 and W
                    - labels (Tensor[N]): the class label for each ground-truth box
                
                The model returns a Dict[Tensor] during training, containing the classification and regression
                losses for both the RPN and the R-CNN.
                """
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

                # train pytorch official faster rcnn
                # train for one epoch, printing every 10 iterations
                train_one_epoch(self.model_ft, optimizer_ft, dataloader, self.device, epoch, print_freq=10)
                # update the learning rate
                optimizer_ft.step()
                # evaluate on the test dataset
                # evaluate(self.model_ft, data_loader_test, device=device)

        if save_model:
            self.save_model()

    def predict_proba(self, data_dir, data_names=None, transform=None, batch_size=1,
                      conf_thres=0.5, nms_thres=0.4, model_type='Faster_RCNN',
                      verbose=True, **kwargs):
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
        result = []
        self.model_ft.eval()
        count = 1
        if model_type == 'Yolov3':
            dataloader = ImageFolder(folder_path=data_dir, img_names=data_names)
            dataloader = torch.utils.data.DataLoader(dataloader)
            for img_path, img in dataloader:
                # Get detections for yolov3
                detections = self.model_ft(img.to(self.device))
                # (x1, y1, x2, y2, object_conf, class_score, class_pred)
                detections = non_max_suppression(
                    detections, conf_thres, nms_thres)
                if verbose:
                    print("Prediction: " + str(count) + '/' + str(len(dataloader)))
                    # print(detections)
                    # print(detections[0].shape)
                    count += 1

                result.append(detections)
        else:
            dataloader = create_img_dataloader(data_dir=data_dir, labels=None, transform=transform,
                                               batch_size=1, shuffle=False, data_names=data_names)
            for batch in dataloader:
                inputs = batch['image'][0]
                # faster rcnn
                """
                During inference, the model requires only the input tensors, and returns the post-processed
                predictions as a List[Dict[Tensor]], one for each input image. The fields of the Dict are as
                follows:
                    - boxes (Tensor[N, 4]): the predicted boxes in [x0, y0, x1, y1] format, with values between
                      0 and H and 0 and W
                    - labels (Tensor[N]): the predicted labels for each image
                    - scores (Tensor[N]): the scores or each prediction
                """
                with torch.no_grad():
                    prediction = self.model_ft([inputs.to(self.device)])
                    if verbose:
                        print("Prediction: " + str(count) + '/' + str(len(dataloader)))
                        count += 1
                        print(prediction)
                    result.append(prediction)
        return result

    def predict(self, data_dir, data_names=None, transform=None, model_type='Faster_RCNN'):
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
        proba_result = self.predict_proba(
            data_dir=data_dir, data_names=data_names, transform=transform, model_type=model_type)
        return proba_result

    def save_model(self):
        # save model
        with open(os.path.join(TRAINED_DEEP_MODEL_DIR, self._proj_id + '_model.pkl'), 'wb') as f:
            pickle.dump(self.model_ft, f)


def _resnet_fpn_backbone(backbone):
    # backbone = resnet.__dict__[backbone_name](
    #     pretrained=pretrained,
    #     norm_layer=misc_nn_ops.FrozenBatchNorm2d)
    # freeze layers
    for name, parameter in backbone.named_parameters():
        if 'layer2' not in name and 'layer3' not in name and 'layer4' not in name:
            parameter.requires_grad_(False)

    return_layers = {'layer1': 0, 'layer2': 1, 'layer3': 2, 'layer4': 3}

    in_channels_stage2 = 256
    in_channels_list = [
        in_channels_stage2,
        in_channels_stage2 * 2,
        in_channels_stage2 * 4,
        in_channels_stage2 * 8,
    ]
    out_channels = 256
    return BackboneWithFPN(backbone, return_layers, in_channels_list, out_channels)


def _init_faster_rcnn(backbone='ResNet', num_classes=91, **kwargs):
    global MODEL_NAME
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    res50 = models.resnet.__dict__['resnet50'](
        pretrained=False,
        norm_layer=misc_nn_ops.FrozenBatchNorm2d)
    res50.load_state_dict(
        torch.load(os.path.join(PRETRAINED_DEEP_MODEL_DIR, 'resnet50-19c8e357.pth'), map_location=device))
    backbone = _resnet_fpn_backbone(res50)

    model = FasterRCNN(backbone, num_classes, **kwargs)
    model.load_state_dict(torch.load(os.path.join(
        PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME['Faster_RCNN']), map_location=device))

    # model.load_state_dict(torch.load(os.path.join(
    #     PRETRAINED_DEEP_MODEL_DIR, MODEL_NAME['Faster_RCNN']), map_location=device))
    return model


def _init_yolov3(num_classes=91, img_size=416, **kwargs):
    from ..third_party.yolov3.models import Darknet
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Initiate model
    subprocess.call(
        os.path.join(file_dir, 'third_party', 'yolov3', 'config', 'create_custom_model.sh') + ' ' + str(num_classes),
        shell=True)
    model = Darknet(os.path.join(file_dir, 'third_party', 'yolov3', 'config', 'yolov3-custom.cfg'),
                    num_classes=num_classes, img_size=img_size).to(device)

    # If specified we start from checkpoint
    # model.load_darknet_weights(os.path.join(
    #     PRETRAINED_DEEP_MODEL_DIR, 'yolov3', 'yolov3.weights'))
    return model
