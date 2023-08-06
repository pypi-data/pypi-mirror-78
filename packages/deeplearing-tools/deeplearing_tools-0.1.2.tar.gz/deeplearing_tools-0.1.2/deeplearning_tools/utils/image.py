from .env import *
if __TORCH_AVAILABLE__:
    import torchvision.transforms as T

import cv2
import numpy as np


def load(path_or_bytes, size=None):
    """
    加载图片
    :param path_or_bytes: 图片目录 / 字节
    :param size: 缩放图片 (width, height)
    :return: 图片 np.array (height, width, dim)
    """
    if isinstance(path_or_bytes, str):
        im = np.fromfile(path_or_bytes, dtype=np.uint8)
    elif isinstance(path_or_bytes, bytes):
        im = np.frombuffer(path_or_bytes, dtype=np.uint8)
    else:
        raise TypeError("image must be path or bytes")

    im = cv2.imdecode(im, -1)
    if size is not None:
        im = cv2.resize(im, size, interpolation=cv2.INTER_AREA)
    return im


def to_rgb(im):
    """
    图片转 RGB
    :param im: 图片 np.array
    :return: 图片 np.array
    """
    if len(im.shape) == 2:  # 灰度
        return cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
    elif im.shape[2] == 4:  # PNG (RGBA)
        return cv2.cvtColor(im, cv2.COLOR_RGBA2RGB)
    assert len(im.shape) == 3 and im.shape[2] == 3  # 如果 Channel 不为3, 肯定出问题了
    return im


def normalize(im, mean, std):
    if isinstance(mean, list):
        mean = tuple(mean)
        return normalize(im, mean, std)
    elif isinstance(mean, float):
        mean = (mean,) * 3
    elif not isinstance(mean, tuple):
        raise TypeError("mean must be tuple of float / float / list of float")
    if len(mean) == 1:
        mean = mean * 3

    if isinstance(std, list):
        std = tuple(std)
        return normalize(im, mean, std)
    elif isinstance(std, float):
        std = (std,) * 3
    elif not isinstance(std, tuple):
        raise TypeError("std must be tuple of float / float / list of float")
    if len(std) == 1:
        std = std * 3

    assert len(mean) == 3
    assert len(std) == 3

    if __TORCH_AVAILABLE__:
        transform = T.Compose([
            T.ToTensor(),
            T.Normalize(mean, std)
        ])
        return transform(im)
    else:
        im = im / 255
        im = np.subtract(im, [[list(mean)]])
        im = np.divide(im, [[list(std)]])
        return im.transpose(2, 0, 1)
