import os
import glob
import torch
import pickle
import numpy as np
from tqdm import tqdm
from typing import List
from torchvision import transforms as T
from torch.utils.data import Dataset
from ..utils import encode, image
from ..utils.label_map import parse_label_map_c2i


class ImageDataset(Dataset):
    def __init__(
            self,
            path: str = './samples',
            transform: T = None,
            extensions: List[str] = None,
            cache: str = None,
            label_map: List[str] = None,
            size: (int, int) = (128, 128),
            pad_to: int = None,
            one_hot: bool = False,
            placeholder: bool = True
    ):
        """
        图片数据集: label_md5.jpg
        :param path: 目录
        :param transform: 预处理
        :param extensions: 图片拓展名
        :param cache: 缓存文件名
        :param label_map: 码表
        :param size: 输出图片尺寸 (h, w)
        :param pad_to: 填充到 (对齐), 为 None 不填充
        :param one_hot: 是否 OneHot 编码
        :param placeholder: 占位符, Index 0
        """
        if extensions is None:
            extensions = ['jpg', 'png', 'bmp']
        if transform is None:
            transform = T.Compose([
                T.ToTensor()
            ])

        self.size = size
        self.label_map = label_map
        self.transform = transform
        self.files = []
        self.pad_to = pad_to
        self.one_hot = one_hot
        self.placeholder = placeholder
        for ext in extensions:
            self.files.extend(glob.glob(os.path.join(path, '*.' + ext)))

        # 启动缓存模式
        self.cache_mode = True if cache is not None else False
        self.cache_path = cache

        if cache:
            if os.path.exists(cache):
                with open(self.cache_path, 'rb') as f:
                    data = pickle.load(f)
                    self.cache = data['cache']
                    self.label_map = data['label_map']
            else:
                self._build_cache()

        # 创建索引
        self._build_label_map()

    def get_label_map(self) -> str:
        return ''.join(self.label_map)

    def _build_label_map(self):
        if not self.label_map:
            self.label_map = []
            for file in self.files:
                label = str(os.path.basename(file).split('_')[0])
                for i in label:
                    if i not in self.label_map:
                        self.label_map.append(i)
            if self.placeholder:
                self.label_map = ['_'] + sorted(self.label_map)
            else:
                self.label_map = sorted(self.label_map)

        self.label_map_length = len(self.label_map)
        self.reverse_label_map = parse_label_map_c2i(self.label_map)

    def _build_cache(self):
        # 先创建 LabelMap
        self._build_label_map()

        self.cache = []
        for file in tqdm(self.files, desc="Building Cache"):
            self.cache.append(self._load_file(file))
        print("Saving Cache")
        with open(self.cache_path, 'wb') as f:
            pickle.dump(dict(cache=self.cache, label_map=self.label_map), f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Cache Saved")

    def _load_file(self, file):
        label = str(os.path.basename(file).split('_')[0])
        label = encode.str_to_tensor(label, self.reverse_label_map)
        im = image.load(file, self.size)
        return im, label

    def __len__(self):
        if self.cache_mode:
            return len(self.cache)
        else:
            return len(self.files)

    def get_mean_std(self):
        mean = np.array([0, 0, 0], dtype=np.float)
        std = np.array([0, 0, 0], dtype=np.float)
        for i in tqdm(range(len(self)), desc="Evaluating Mean & Std"):
            im, _ = self._get_from_cache(i)
            im = im.astype(np.float32) / 255.
            for j in range(3):
                mean[j] += im[:, :, j].mean()
                std[j] += im[:, :, j].std()

        mean, std = mean / len(self), std / len(self)
        return mean, std

    def _get_from_cache(self, item):
        if self.cache_mode:
            return self.cache[item]
        else:
            return self._load_file(self.files[item])

    def __getitem__(self, item):
        """
        取样本
        :param item: ID
        :return: 图片, 标签, 标签长度
        """
        # label tensor([19, 15,  5, 28])
        im, label = self._get_from_cache(item)
        im = self.transform(im)
        raw_len = int(len(label))
        if self.pad_to is not None and raw_len < self.pad_to:
            pad = torch.IntTensor([0] * (self.pad_to - raw_len)).to(torch.int64)
            label = torch.cat([label, pad])
        if self.one_hot:
            label = encode.one_hot_encode(label, self.label_map_length)
        return im, label, raw_len
