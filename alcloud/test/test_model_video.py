import torch
import mmcv
import os
import logging
from abc import ABCMeta, abstractmethod

from alcloud.config import PRETRAINED_DEEP_MODEL_DIR

from mmcv.runner import load_checkpoint
from mmcv.parallel import MMDataParallel

# from mmaction.datasets import build_dataloader
# from mmaction.models.builder import build_recognizer
# from mmaction.models.recognizers import TSN3D

def single_test(model, data_loader):
    model.eval()
    results = []
    dataset = data_loader.dataset
    prog_bar = mmcv.ProgressBar(len(dataset))
    for i, data in enumerate(data_loader):
        with torch.no_grad():
            result = model(return_loss=False, **data)
        results.append(result)

        batch_size = data['img_group_0'].data[0].size(0)
        for _ in range(batch_size):
            prog_bar.update()
    return results

file_dir = os.path.dirname(__file__)
parent, _ = os.path.split(file_dir)

cfg = mmcv.Config.fromfile(os.path.join(parent, 'alcloud', 'third_party', 'mmaction_configs', 'kinetics400', 'i3d_kinetics400_3d_rgb_r50_c3d_inflate3x1x1_seg1_f32s2_video.py'))
# model = build_recognizer(
#     cfg.model, train_cfg=None, test_cfg=cfg.test_cfg)

import torch.nn as nn


class Registry(object):

    def __init__(self, name):
        self._name = name
        self._module_dict = dict()

    @property
    def name(self):
        return self._name

    @property
    def module_dict(self):
        return self._module_dict

    def _register_module(self, module_class):
        """Register a module

        Args:
            module (:obj:`nn.Module`): Module to be registered.
        """
        if not issubclass(module_class, nn.Module):
            raise TypeError(
                'module must be a child of nn.Module, but got {}'.format(
                    module_class))
        module_name = module_class.__name__
        if module_name in self._module_dict:
            raise KeyError('{} is already registered in {}'.format(
                module_name, self.name))
        self._module_dict[module_name] = module_class

    def register_module(self, cls):
        self._register_module(cls)
        return cls


BACKBONES = Registry('backbone')
FLOWNETS = Registry('flownet')
SPATIAL_TEMPORAL_MODULES = Registry('spatial_temporal_module')
SEGMENTAL_CONSENSUSES = Registry('segmental_consensus')
HEADS = Registry('head')
RECOGNIZERS = Registry('recognizer')
LOCALIZERS = Registry('localizer')
DETECTORS = Registry('detector')
ARCHITECTURES = Registry('architecture')
NECKS = Registry('neck')
ROI_EXTRACTORS = Registry('roi_extractor')


def _build_module(cfg, registry, default_args):
    assert isinstance(cfg, dict) and 'type' in cfg
    assert isinstance(default_args, dict) or default_args is None
    args = cfg.copy()
    obj_type = args.pop('type')
    if mmcv.is_str(obj_type):
        if obj_type not in registry.module_dict:
            raise KeyError('{} is not in the {} registry'.format(
                obj_type, registry.name))
        obj_type = registry.module_dict[obj_type]
    elif not isinstance(obj_type, type):
        raise TypeError('type must be a str or valid type, but got {}'.format(
            type(obj_type)))
    if default_args is not None:
        for name, value in default_args.items():
            args.setdefault(name, value)
    return obj_type(**args)


def build(cfg, registry, default_args=None):
    if isinstance(cfg, list):
        modules = [_build_module(cfg_, registry, default_args) for cfg_ in cfg]
        return nn.Sequential(*modules)
    else:
        return _build_module(cfg, registry, default_args)


def build_backbone(cfg):
    return build(cfg, BACKBONES)


def build_flownet(cfg):
    return build(cfg, FLOWNETS)


def build_spatial_temporal_module(cfg):
    return build(cfg, SPATIAL_TEMPORAL_MODULES)


def build_segmental_consensus(cfg):
    return build(cfg, SEGMENTAL_CONSENSUSES)


def build_head(cfg):
    return build(cfg, HEADS)


def build_recognizer(cfg, train_cfg=None, test_cfg=None):
    return build(cfg, RECOGNIZERS,
                 dict(train_cfg=train_cfg, test_cfg=test_cfg))


def build_localizer(cfg, train_cfg=None, test_cfg=None):
    return build(cfg, LOCALIZERS, dict(train_cfg=train_cfg, test_cfg=test_cfg))


def build_detector(cfg, train_cfg=None, test_cfg=None):
    return build(cfg, DETECTORS, dict(train_cfg=train_cfg, test_cfg=test_cfg))


def build_architecture(cfg, train_cfg=None, test_cfg=None):
    return build(cfg, ARCHITECTURES,
                 dict(train_cfg=train_cfg, test_cfg=test_cfg))


def build_neck(cfg):
    return build(cfg, NECKS)


def build_roi_extractor(cfg):
    return build(cfg, ROI_EXTRACTORS)


class BaseRecognizer(nn.Module):
    """Base class for recognizers"""

    __metaclass__ = ABCMeta

    def __init__(self):
        super(BaseRecognizer, self).__init__()

    @property
    def with_tenon_list(self):
        return hasattr(self, 'tenon_list') and self.tenon_list is not None

    @property
    def with_cls(self):
        return hasattr(self, 'cls_head') and self.cls_head is not None

    @abstractmethod
    def forward_train(self, num_modalities, **kwargs):
        pass

    @abstractmethod
    def forward_test(self, num_modalities, **kwargs):
        pass

    def init_weights(self, pretrained=None):
        if pretrained is not None:
            logger = logging.getLogger()
            logger.info("load model from: {}".format(pretrained))

    def forward(self, num_modalities, img_meta, return_loss=True, **kwargs):
        num_modalities = int(num_modalities[0])
        if return_loss:
            return self.forward_train(num_modalities, img_meta, **kwargs)
        else:
            return self.forward_test(num_modalities, img_meta, **kwargs)


class TSN3D(BaseRecognizer):

    def __init__(self,
                 backbone,
                 flownet=None,
                 spatial_temporal_module=None,
                 segmental_consensus=None,
                 cls_head=None,
                 train_cfg=None,
                 test_cfg=None,
                 **kwargs):

        super(TSN3D, self).__init__()
        self.backbone = build_backbone(backbone)

        if flownet is not None:
            self.flownet = build_flownet(flownet)

        if spatial_temporal_module is not None:
            self.spatial_temporal_module = build_spatial_temporal_module(
                spatial_temporal_module)
        else:
            raise NotImplementedError

        if segmental_consensus is not None:
            self.segmental_consensus = build_segmental_consensus(
                segmental_consensus)
        else:
            raise NotImplementedError

        if cls_head is not None:
            self.cls_head = build_head(cls_head)
        else:
            raise NotImplementedError

        self.train_cfg = train_cfg
        self.test_cfg = test_cfg

        self.init_weights()

    @property
    def with_flownet(self):
        return hasattr(self, 'flownet') and self.flownet is not None

    @property
    def with_spatial_temporal_module(self):
        return hasattr(self, 'spatial_temporal_module') and self.spatial_temporal_module is not None

    @property
    def with_segmental_consensus(self):
        return hasattr(self, 'segmental_consensus') and self.segmental_consensus is not None

    @property
    def with_cls_head(self):
        return hasattr(self, 'cls_head') and self.cls_head is not None

    def init_weights(self):
        super(TSN3D, self).init_weights()
        self.backbone.init_weights()

        if self.with_flownet:
            self.flownet.init_weights()

        if self.with_spatial_temporal_module:
            self.spatial_temporal_module.init_weights()

        if self.with_segmental_consensus:
            self.segmental_consensus.init_weights()

        if self.with_cls_head:
            self.cls_head.init_weights()

    def extract_feat_with_flow(self, img_group,
                               trajectory_forward=None,
                               trajectory_backward=None):
        x = self.backbone(img_group,
                          trajectory_forward=trajectory_forward,
                          trajectory_backward=trajectory_backward)
        return x

    def extract_feat(self, img_group):
        x = self.backbone(img_group)
        return x

    def forward_train(self,
                      num_modalities,
                      img_meta,
                      gt_label,
                      **kwargs):
        assert num_modalities == 1
        img_group = kwargs['img_group_0']

        bs = img_group.shape[0]
        img_group = img_group.reshape((-1, ) + img_group.shape[2:])
        num_seg = img_group.shape[0] // bs

        if self.with_flownet:
            if self.flownet.multiframe:
                img_forward = img_group[:, :, 1:, :, :]
                if self.flownet.flip_rgb:
                    img_forward = img_forward.flip(1)
                img_forward = img_forward.transpose(1, 2).contiguous().view(
                    (img_forward.size(0), -1,
                     img_forward.size(3), img_forward.size(4)))
                trajectory_forward, photometric_forward, ssim_forward, smooth_forward = self.flownet(
                    img_forward)
                img_backward = img_group.flip(2)[:, :, 1:, :, :]
                if self.flownet.rgb_disorder:
                    img_backward = img_backward.flip(1)
                img_backward = img_backward.transpose(1, 2).contiguous().view(
                    (img_backward.size(0), -1,
                     img_backward.size(3), img_backward.size(4)))
                trajectory_backward, photometric_backward, ssim_backward, smooth_backward = self.flownet(
                    img_backward)
            else:
                # TODO: Wrap it into a function, e.g. ImFlows2ImFlowStack
                num_frames = img_group.size(2)
                traj_forwards, traj_backwards = [], []
                photometric_forwards, photometric_backwards = [], []
                ssim_forwards, ssim_backwards = [], []
                smooth_forwards, smooth_backwards = [], []
                for i in range(1, num_frames - 1):
                    img_forward = img_group[:, :, i:i+2, :, :]
                    if self.flownet.flip_rgb:
                        img_forward = img_forward.flip(1)
                    img_forward = img_forward.transpose(1, 2).contiguous().view(
                        (img_forward.size(0), -1,
                         img_forward.size(3), img_forward.size(4)))
                    traj_forward, photometric_forward, ssim_forward, smooth_forward = self.flownet(
                        img_forward)
                    traj_forwards.append(traj_forward)
                    photometric_forwards.append(photometric_forward)
                    ssim_forwards.append(ssim_forward)
                    smooth_forwards.append(smooth_forward)
                    img_backward = img_group[
                        :, :,
                        num_frames - i - 1: num_frames - i + 1, :, :].flip(2)
                    if self.flownet.flip_rgb:
                        img_backward = img_backward.flip(1)
                    img_backward = img_backward.transpose(1, 2).contiguous().view(
                        (img_backward.size(0), -1,
                         img_backward.size(3), img_backward.size(4)))
                    traj_backward, photometric_backward, ssim_backward, smooth_backward = self.flownet(
                        img_backward)
                    traj_backwards.append(traj_backward)
                    photometric_backwards.append(photometric_backward)
                    ssim_backwards.append(ssim_backward)
                    smooth_backwards.append(smooth_backward)

                def _organize_trajectories(trajectory_lvls_pairs):
                    res = [[]] * len(trajectory_lvls_pairs[0])
                    for trajectory_lvls in trajectory_lvls_pairs:
                        for i, trajectory in enumerate(trajectory_lvls):
                            res[i].append(trajectory)
                    for i in range(len(trajectory_lvls_pairs[0])):
                        res[i] = torch.cat(res[i], 1)
                    return tuple(res)

                def _organize_loss_outs(loss_outs_lvls_pairs):
                    L = len(loss_outs_lvls_pairs)
                    num_level = len(loss_outs_lvls_pairs[0])
                    num_item = len(loss_outs_lvls_pairs[0][0])
                    res = []
                    for i in range(num_level):
                        res_level = []
                        for j in range(num_item):
                            outs = []
                            for k in range(L):
                                outs.append(loss_outs_lvls_pairs[k][i][j])
                            res_level.append(outs)
                        res.append(res_level)
                    for i in range(num_level):
                        for j in range(num_item):
                            res[i][j] = torch.cat(res[i][j], 1)
                        res[i] = tuple(res[i])
                    return tuple(res)

                trajectory_forward = _organize_trajectories(traj_forwards)
                trajectory_backward = _organize_trajectories(traj_backwards)
                photometric_forward = _organize_loss_outs(photometric_forwards)
                photometric_backward = _organize_loss_outs(
                    photometric_backwards)
                ssim_forward = _organize_loss_outs(ssim_forwards)
                ssim_backward = _organize_loss_outs(ssim_backwards)
                smooth_forward = _organize_loss_outs(smooth_forwards)
                smooth_backward = _organize_loss_outs(smooth_backwards)

            x = self.extract_feat_with_flow(
                img_group[:, :, 1:-1, :, :],
                trajectory_forward=trajectory_forward,
                trajectory_backward=trajectory_backward)
        else:
            x = self.extract_feat(img_group)
        if self.with_spatial_temporal_module:
            x = self.spatial_temporal_module(x)
        if self.with_segmental_consensus:
            x = x.reshape((-1, num_seg) + x.shape[1:])
            x = self.segmental_consensus(x)
            x = x.squeeze(1)
        losses = dict()
        if self.with_flownet:
            losses.update(self.flownet.loss(photometric_forward,
                                            ssim_forward, smooth_forward,
                                            direction='forward'))
            losses.update(self.flownet.loss(photometric_backward,
                                            ssim_backward, smooth_backward,
                                            direction='backward'))
        if self.with_cls_head:
            cls_score = self.cls_head(x)
            gt_label = gt_label.squeeze()
            loss_cls = self.cls_head.loss(cls_score, gt_label)
            losses.update(loss_cls)

        return losses

    def forward_test(self,
                     num_modalities,
                     img_meta,
                     **kwargs):
        assert num_modalities == 1
        img_group = kwargs['img_group_0']

        bs = img_group.shape[0]
        img_group = img_group.reshape((-1, ) + img_group.shape[2:])
        num_seg = img_group.shape[0] // bs

        if self.with_flownet:
            if self.flownet.multiframe:
                img_forward = img_group[:, :, 1:, :, :]
                if self.flownet.flip_rgb:
                    img_forward = img_forward.flip(1)
                img_forward = img_forward.transpose(1, 2).contiguous().view(
                    (img_forward.size(0), -1,
                     img_forward.size(3), img_forward.size(4)))
                trajectory_forward, _, _, _ = self.flownet(
                    img_forward, train=False)
                img_backward = img_group.flip(2)[:, :, 1:, :, :]
                if self.flownet.flip_rgb:
                    img_backward = img_backward.flip(1)
                img_backward = img_backward.transpose(1, 2).contiguous().view(
                    (img_backward.size(0), -1,
                     img_backward.size(3), img_backward.size(4)))
                trajectory_backward, _, _, _ = self.flownet(
                    img_backward, train=False)
            else:
                # TODO: Wrap it into a function, e.g. ImFlows2ImFlowStack
                num_frames = img_group.size(2)
                traj_forwards, traj_backwards = [], []
                for i in range(1, num_frames - 1):
                    img_forward = img_group[:, :, i:i+2, :, :]
                    if self.flownet.rgb_disorder:
                        img_forward = img_forward.flip(1)
                    img_forward = img_forward.transpose(1, 2).contiguous().view(
                        (img_forward.size(0), -1,
                         img_forward.size(3), img_forward.size(4)))
                    traj_forward, _, _, _ = self.flownet(
                        img_forward, train=False)
                    traj_forwards.append(traj_forward)
                    img_backward = img_group[
                        :, :, num_frames - i - 1:
                        num_frames - i + 1, :, :].flip(2)
                    if self.flownet.rgb_disorder:
                        img_backward = img_backward.flip(1)
                    img_backward = img_backward.transpose(1, 2).contiguous().view(
                        (img_backward.size(0), -1,
                         img_backward.size(3), img_backward.size(4)))
                    traj_backward, _, _, _ = self.flownet(
                        img_backward, train=False)
                    traj_backwards.append(traj_backward)

                def _organize_trajectories(trajectory_lvls_pairs):
                    res = [[]] * len(trajectory_lvls_pairs[0])
                    for trajectory_lvls in trajectory_lvls_pairs:
                        for i, trajectory in enumerate(trajectory_lvls):
                            res[i].append(trajectory)
                    for i in range(len(trajectory_lvls_pairs[0])):
                        res[i] = torch.cat(res[i], 1)
                    return tuple(res)

                trajectory_forward = _organize_trajectories(traj_forwards)
                trajectory_backward = _organize_trajectories(traj_backwards)

            x = self.extract_feat_with_flow(
                img_group[:, :, 1:-1, :, :],
                trajectory_forward=trajectory_forward,
                trajectory_backward=trajectory_backward)
        else:
            x = self.extract_feat(img_group)
        if self.with_spatial_temporal_module:
            x = self.spatial_temporal_module(x)
        if self.with_segmental_consensus:
            x = x.reshape((-1, num_seg) + x.shape[1:])
            x = self.segmental_consensus(x)
            x = x.squeeze(1)
        if self.with_cls_head:
            x = self.cls_head(x)

        return x.cpu().numpy()



default_args = dict(train_cfg=None, test_cfg=cfg.test_cfg)
args = cfg.model.copy()
# obj_type = args.pop('type')
# obj_type = Registry('recognizer').module_dict[obj_type]
if default_args is not None:
    for name, value in default_args.items():
        args.setdefault(name, value)
model = TSN3D(**args)


load_checkpoint(model, os.path.join(PRETRAINED_DEEP_MODEL_DIR, 'video', 'i3d_r50_f32s2_k400-2c57e077.pth'), strict=True)
model = MMDataParallel(model, device_ids=[0])

data_loader = build_dataloader(
    dataset,
    imgs_per_gpu=1,
    workers_per_gpu=cfg.data.workers_per_gpu,
    num_gpus=1,
    dist=False,
    shuffle=False)
outputs = single_test(model, data_loader)
