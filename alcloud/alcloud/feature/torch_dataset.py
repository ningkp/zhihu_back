import os
import torch
import numpy as np

from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T
from torchvision.datasets import MNIST

__all__ = [
    'ImgDataset',
    'ObjDetDataset',
]


class ImgDataset(Dataset):
    '''Create a pytorch dataset.

    Parameters
    ----------
    data_dir: str
        Path to the data folder.

    trans: torchvision.transforms.Compose
        Transform object which will be applied to the data.

    labels: dict, optional (default=None)
        The labels of dataset.
        Key: file name
        Value: label

    data_names: list, optional (default=None)
        The data names. If not specified, it will all the files in the
        data_dir.

    check_validity: bool, optional (default=True)
        Whether to check the validity of parameters. (Maybe time consuming)
    '''

    def __init__(self, data_dir, trans=None, labels=None, data_names=None, check_validity=True):
        self._data_dir = data_dir
        self._trans = trans
        if not data_names:
            self._data_list = os.listdir(self._data_dir)
        else:
            assert isinstance(data_names, list)
            # check the names' validity.
            if check_validity:
                all_names = os.listdir(self._data_dir)
                for name in data_names:
                    assert name in all_names, 'File name {} is not in the data dir {}'.format(str(name), str(all_names))
            self._data_list = data_names
        if check_validity:
            for name in self._data_list:
                ext = name.split('.')[-1]
                assert ext.lower() in ['jpg', 'jpeg',
                                       'png'], 'file {} has an unexpected extension {}. Valide extensions are {}'.format(
                    name, ext, str(['jpg', 'jpeg', 'png']))
        self._labels = None
        if labels:
            assert isinstance(labels, dict)
            self._labels = labels
            self._data_ind = dict(zip(self._data_list, range(len(self._data_list))))
            self._label_ind = dict(zip(range(len(self._labels)), self._labels.keys()))

    def __len__(self):
        if self._labels:
            return len(self._labels)
        else:
            return len(self._data_list)

    def __getitem__(self, index):
        if self._labels:
            data_names = self._label_ind[index]
            data_ind = self._data_ind[data_names]
            label = self._labels[data_names]
        else:
            data_ind = index

        image = Image.open(os.path.abspath(os.path.join(self._data_dir, self._data_list[data_ind])))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        if image.width>1024 or image.height>1024:
            whr = image.width/image.height
            if image.width > image.height:
                image = image.resize((1024, round(1024/whr)))
            else:
                image = image.resize((round(1024*whr), 1024))

        if self._trans:
            image = self._trans(image)

        if self._labels:
            return {'image': image, 'image_name': data_names, 'target': label}
        else:
            return {'image': image, 'image_name': self._data_list[index]}


class ObjDetDataset(torch.utils.data.Dataset):
    """
    img_names : list
        list of img names.

    label_dict: dict
        key: img file name
        value: list [[label_idx x0 y0 x1 y1], ...]
    """
    def __init__(self, root, img_names=None, label_dict=None, transforms=None):
        self.root = root
        self.transforms = transforms
        self._label_flag = False
        # load all image files, sorting them to
        # ensure that they are aligned
        # self.imgs = list(sorted(os.listdir(os.path.join(root, "PNGImages"))))
        # self.masks = list(sorted(os.listdir(os.path.join(root, "PedMasks"))))
        if label_dict is not None:
            assert isinstance(label_dict, dict)
            self.imgs = list(label_dict.keys())
            self.label_dict = label_dict
            self._label_flag = True
        else:
            if img_names:
                self.imgs = img_names
            else:
                self.imgs = os.listdir(root)

    def __getitem__(self, idx):
        """
        target: a dict containing the following fields
        boxes (FloatTensor[N, 4]): the coordinates of the N bounding boxes in [x0, y0, x1, y1] format, ranging from 0 to W and 0 to H
        labels (Int64Tensor[N]): the label for each bounding box
        image_id (Int64Tensor[1]): an image identifier. It should be unique between all the images in the dataset, and is used during evaluation
        area (Tensor[N]): The area of the bounding box. This is used during evaluation with the COCO metric, to separate the metric scores between small, medium and large boxes.
        iscrowd (UInt8Tensor[N]): instances with iscrowd=True will be ignored during evaluation.
        (optionally) masks (UInt8Tensor[N, H, W]): The segmentation masks for each one of the objects
        (optionally) keypoints (FloatTensor[N, K, 3]): For each one of the N objects, it contains the K keypoints in [x, y, visibility] format, defining the object. visibility=0 means that the keypoint is not visible. Note that for data augmentation, the notion of flipping a keypoint is dependent on the data representation, and you should probably adapt references/detection/transforms.py for your new keypoint representation

        :param idx:
        :return:
        """
        # load images ad masks
        # img_path = os.path.join(self.root, "PNGImages", self.imgs[idx])
        # mask_path = os.path.join(self.root, "PedMasks", self.masks[idx])
        img_path = os.path.join(self.root, self.imgs[idx])
        img = Image.open(img_path)
        # Handle images with less than three channels
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # note that we haven't converted the mask to RGB,
        # because each color corresponds to a different instance
        # with 0 being background
        # mask = Image.open(mask_path)

        # mask = np.array(mask)
        # instances are encoded as different colors
        # obj_ids = np.unique(mask)
        # first id is the background, so remove it
        # obj_ids = obj_ids[1:]

        # split the color-encoded mask into a set
        # of binary masks
        # masks = mask == obj_ids[:, None, None]

        if not self._label_flag:
            return T.ToTensor()(img)

        # get bounding box coordinates for each mask
        obj_ids = self.label_dict[self.imgs[idx]]
        num_objs = len(obj_ids)
        boxes = []
        labels = []
        for i in range(num_objs):
            # pos = np.where(masks[i])
            xmin = np.min(obj_ids[i][1])
            xmax = np.max(obj_ids[i][3])
            ymin = np.min(obj_ids[i][2])
            ymax = np.max(obj_ids[i][4])
            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(obj_ids[i][0])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.as_tensor(labels, dtype=torch.int64)
        # masks = torch.as_tensor(masks, dtype=torch.uint8)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        # target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)

