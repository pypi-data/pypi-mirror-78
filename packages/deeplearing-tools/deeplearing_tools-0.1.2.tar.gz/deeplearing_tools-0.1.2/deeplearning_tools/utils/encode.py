from .env import *
if __TORCH_AVAILABLE__:
    import torch
    import torch.nn.functional as F

import numpy as np
from .label_map import parse_label_map_i2c, parse_label_map_c2i

__all__ = ['one_hot_encode', 'one_hot_decode', 'str_to_tensor', 'tensor_to_str', 'ctc_to_str']


def str_to_tensor(label: str, label_map):
    """
    文本编码
    :param label: 标签文本
    :param label_map: 码表
    :return: 编码后的文本
    """
    label_map = parse_label_map_c2i(label_map)
    data = [label_map[c] for c in label]
    if __TORCH_AVAILABLE__:
        return torch.as_tensor(data).long()
    else:
        return np.array(data, dtype=np.long)


def tensor_to_str(data, label_map):
    """
    文本解码
    :param data: 编码后的文本
    :param label_map: 码表
    :return: 解码后文本
    """
    label_map = parse_label_map_i2c(label_map)
    return ''.join([label_map[int(i)] for i in list(data)])


def ctc_to_str(data, label_map):
    """
    CTC 解码
    :param data: 编码后的文本
    :param label_map: 码表
    :return: 解码后文本
    """
    result = []
    last = -1
    for i in list(data):
        if i == 0:
            last = -1
        elif i != last:
            result.append(i)
            last = i
    return tensor_to_str(result, label_map)


def one_hot_encode(label_tensor, label_map_length):
    """
    OneHot 编码
    :param label_tensor: 标签 Tensor
    :param label_map_length: 码表长度
    :return:
    """
    if __TORCH_AVAILABLE__:
        return F.one_hot(label_tensor, num_classes=label_map_length).float()
    else:
        targets = np.array(label_tensor).reshape(-1)
        return np.eye(label_map_length)[targets]


def one_hot_decode(data):
    """
    OneHot 解码
    :param data: OneHot 编码后的 Tensor
    :return: 解码后的 Tensor
    """
    if __TORCH_AVAILABLE__:
        return torch.argmax(data, dim=1)
    else:
        return np.argmax(data, axis=1)
