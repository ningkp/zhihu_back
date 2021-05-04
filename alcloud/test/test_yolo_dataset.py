import os
import torch
from alcloud.config import TEST_RES_DIR
from alcloud.third_party.yolov3.utils.datasets import ImgObjDetDataset, ImageFolder


# Get dataloader
dataset = ImgObjDetDataset(os.path.join(r'D:\code\PyTorch-YOLOv3-master\data\custom', 'images'), os.path.join(r'D:\code\PyTorch-YOLOv3-master\data\custom', 'labels'), augment=True, multiscale=False)
dataloader = torch.utils.data.DataLoader(
    dataset,
    batch_size=1,
    shuffle=True,
    num_workers=0,
    pin_memory=True,
    collate_fn=dataset.collate_fn,
)

for _, imgs, targets in dataloader:
    print(imgs)
    print(targets)

