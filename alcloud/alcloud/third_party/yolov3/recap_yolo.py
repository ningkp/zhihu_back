from __future__ import division
from models import *
from utils.logger import *
from utils.utils import *
from utils.datasets import *
from utils.parse_config import *
from test import evaluate

from terminaltables import AsciiTable

import os
import sys
import time
import datetime
import argparse

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms
from torch.autograd import Variable
import torch.optim as optim

__all__ = [
    'get_pretrained_yolov3',
]


def get_pretrained_yolov3():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Initiate model
    model = Darknet('./config/yolov3.cfg').to(device)

    # If specified we start from checkpoint
    if opt.pretrained_weights:
        if opt.pretrained_weights.endswith(".pth"):
            model.load_state_dict(torch.load(opt.pretrained_weights))
        else:
            model.load_darknet_weights(opt.pretrained_weights)
    return model


def train_yolov3(model, train_path, epochs=100,
                 img_size=416, batch_size=8, n_cpu=8,
                 gradient_accumulations=2, multiscale_training=True,
                 optimizer=None):
    """
    Train yolov3 model. Use Adam
    """
    # Get dataloader
    dataset = ListDataset(train_path, augment=True,
                          multiscale=multiscale_training)
    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=n_cpu,
        pin_memory=True,
        collate_fn=dataset.collate_fn,
    )

    if not optimizer:
        optimizer = torch.optim.Adam(model.parameters())
    else:
        assert isinstance(optimizer, torch.optim.Optimizer)

    for epoch in range(epochs):
    model.train()
    for batch_i, (_, imgs, targets) in enumerate(dataloader):
        batches_done = len(dataloader) * epoch + batch_i

        imgs = Variable(imgs.to(device))
        targets = Variable(targets.to(device), requires_grad=False)

        loss, outputs = model(imgs, targets)
        loss.backward()

        if batches_done % gradient_accumulations:
            # Accumulates gradient before each step
            optimizer.step()
            optimizer.zero_grad()
