import os
from typing import List
from torchvision import transforms as T
from torch.utils.data import Dataset
from ..utils import image


class DetectionDataset(Dataset):
    def __init__(
            self,
            path: str = './samples',
            path_txt: str='labels',
            transform: T = None,
            extensions: List[str] = None,
            size: (int, int) = (128, 128)
    ):
        """
        目标数据集, 不可直接使用, tensor 未对齐
        :param path: 目录
        :param transform: 预处理
        :param extensions: 图片拓展名
        :param size: 输出图片尺寸 (w, h)
        """

        if extensions is None:
            extensions = ['jpg', 'png', 'bmp']
        if transform is None:
            transform = T.Compose([
                T.ToTensor()
            ])
        self.path_txt = path_txt
        self.size = size
        self.transform = transform
        # self.files = []

        # for ext in extensions:
        #     self.files.extend(glob.glob(os.path.join(path, '*.' + ext)))
        self.images_files = [os.path.join(path,i) for i in os.listdir(path)]
        # self.labels_files = [os.path.join(path_txt,i) for i in os.listdir(path_txt)]

        
    def __len__(self):
        return len(self.images_files)

    def __getitem__(self, item):
        file_name = os.path.basename(self.images_files[item])
        
        labels_path = os.path.join(self.path_txt,file_name.replace('.jpg','.txt'))
        with open(labels_path,'r')as f:
            result = f.readlines()
        boxes = []
        for i in result:
            box = tuple([float(k) for k in i.strip().split(' ')[1:]])
            boxes.append(box)
        # print(boxes)
        # boxes = [tuple(map(int, item.split(","))) for item in file_name.split("_")[:-1]]
        # print(boxes) [(60, 327, 28, 85), (273, 287, 63, 12)]
        im = image.load(self.images_files[item], size=self.size)
        return im, boxes

