import torch
from torch.utils.data import Dataset
from torchvision import transforms

from ..utils.detection import transforms as T
from .torch_dataset import ImgDataset, ObjDetDataset
from ..utils.detection.utils import collate_fn

__all__ = ['create_img_dataloader',
           'load_feature_label',
           ]


def create_img_dataloader(data_dir, labels=None, batch_size=1,
                          transform=None, shuffle=False, data_names=None,
                          check_validity=True):
    '''Create a pytorch img DataLoader object.

    :param data_dir: str
        Path to the data folder.

    :param labels: dict, optional (default=None)
        The labels of dataset.
        Key: file name
        Value: label

    :param batch_size: int, optional (default=1)
        Batch size when training.

    :param transform: torchvision.transforms.Compose, optional (default=None)
        Transforms object that will be applied to the image data.

    :param shuffle: bool, optional (default=False)
        Whether shuffle the data.

    :param data_names: list, optional (default=None)
        The data names. If not specified, it will all the files in the
        data_dir.

    :param check_validity: bool, optional (default=True)
        Whether to check the validity of parameters. (Maybe time consuming)

    :return: dataloader: torch.utils.data.DataLoader
        Dataloader object created from the given data dir.
    '''
    if not transform:
        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                  std=[0.229, 0.224, 0.225])])

    img_data = ImgDataset(data_dir=data_dir, trans=transform, labels=labels,
                          data_names=data_names, check_validity=check_validity)
    dataloader = torch.utils.data.DataLoader(img_data, batch_size=batch_size, shuffle=shuffle)
    return dataloader


def load_feature_label(project_id, load_label=False, labeled_index=None, **kwargs):
    '''

    :param project_id: str
        project_id

    :param load_label: bool
        Whether load labels.

    :param labeled_index: array
        The labeled indexex.
        If load_label, this parameter must be provided.

    :return: X: np.ndarray
        feature matrix of all data.

    :return: y: np.ndarray
        labels of labeled index.
    '''
    pass


def create_faster_rcnn_dataloader(data_dir, label_dict=None, batch_size=1,
                          transform=None, shuffle=False, data_names=None, augment=False,
                          num_workers=0, **kwargs):
    """
    label_dict: dict
        key: file name
        value: list [[label_idx x0 y0 x1 y1], ...]
    """
    if transform is None:
        tr = [T.ToTensor()]
        if augment:
            tr.append(T.RandomHorizontalFlip(0.5))
        transform = T.Compose(tr)
    img_data = ObjDetDataset(root=data_dir, transforms=transform, label_dict=label_dict, img_names=data_names)
    dataloader = torch.utils.data.DataLoader(img_data, batch_size=batch_size, shuffle=shuffle,
                                             num_workers=num_workers, collate_fn=collate_fn)
    return dataloader

