import torch
import numpy as np
from torch import nn
from lengyue_dl.backbone import mbv3_small
from lengyue_dl.module import CBAModule, UpSampleModule


# SSH Context Module
class ContextModule(nn.Module):
    def __init__(self, in_channels):
        super(ContextModule, self).__init__()

        block_wide = in_channels // 4
        self.inconv = CBAModule(in_channels, block_wide, 3, 1, padding=1)
        self.upconv = CBAModule(block_wide, block_wide, 3, 1, padding=1)
        self.downconv = CBAModule(block_wide, block_wide, 3, 1, padding=1)
        self.downconv2 = CBAModule(block_wide, block_wide, 3, 1, padding=1)

    def forward(self, x):
        x = self.inconv(x)
        up = self.upconv(x)
        down = self.downconv(x)
        down = self.downconv2(down)
        return torch.cat([up, down], dim=1)


# SSH Detect Module
class DetectModule(nn.Module):
    def __init__(self, in_channels):
        super(DetectModule, self).__init__()

        self.upconv = CBAModule(in_channels, in_channels // 2, 3, 1, padding=1)
        self.context = ContextModule(in_channels)

    def forward(self, x):
        up = self.upconv(x)
        down = self.context(x)
        return torch.cat([up, down], dim=1)


# Job Head Module
class HeadModule(nn.Module):
    def __init__(self, in_channels, out_channels, has_ext=False):
        super(HeadModule, self).__init__()
        self.head = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        self.has_ext = has_ext

        if has_ext:
            self.ext = CBAModule(in_channels, in_channels, kernel_size=3, padding=1, bias=False)

    def init_normal(self, std, bias):
        nn.init.normal_(self.head.weight, std=std)
        nn.init.constant_(self.head.bias, bias)

    def forward(self, x):

        if self.has_ext:
            x = self.ext(x)
        return self.head(x)


# CenterNet Model
class CenterNet(nn.Module):
    """
    CenterNet 模型, 目前只支持 MBV3
    """
    def __init__(self, wide=64, has_ext=True, up_mode="UCBA"):
        super(CenterNet, self).__init__()
        # define backbone
        # self.bb = Mbv3SmallFast()
        self.backbone = mbv3_small(keep=[1, 3, 8, 10], run_to=10)

        # Get the number of branch node channels
        # stride4, stride8, stride16
        c0, c1, c2 = [16, 24, 48]
        # c0, c1, c2 = self.bb.uplayer_shape
        # self.bb.output_channels
        self.conv3 = CBAModule(96, wide, kernel_size=1, stride=1, padding=0, bias=False)  # s32
        self.connect0 = CBAModule(c0, wide, kernel_size=1)  # s4
        self.connect1 = CBAModule(c1, wide, kernel_size=1)  # s8
        self.connect2 = CBAModule(c2, wide, kernel_size=1)  # s16

        self.up0 = UpSampleModule(wide, wide, kernel_size=2, stride=2, mode=up_mode)  # s16
        self.up1 = UpSampleModule(wide, wide, kernel_size=2, stride=2, mode=up_mode)  # s8
        self.up2 = UpSampleModule(wide, wide, kernel_size=2, stride=2, mode=up_mode)  # s4
        self.detect = DetectModule(wide)

        self.center = HeadModule(wide, 1, has_ext=has_ext)
        self.box = HeadModule(wide, 4, has_ext=has_ext)

    def init_weights(self):

        # Set the initial probability to avoid overflow at the beginning
        prob = 0.01
        d = -np.log((1 - prob) / prob)  # -2.19

        # Load backbone weights from ImageNet
        self.bb.load_pretrain()
        self.center.init_normal(0.001, d)
        self.box.init_normal(0.001, 0)

    def load(self, file):
        checkpoint = torch.load(file, map_location="cpu")
        self.load_state_dict(checkpoint)

    def forward(self, x):
        s4, s8, s16, s32 = self.backbone(x)

        s32 = self.conv3(s32)

        s16 = self.up0(s32) + self.connect2(s16)
        s8 = self.up1(s16) + self.connect1(s8)
        s4 = self.up2(s8) + self.connect0(s4)
        x = self.detect(s4)

        center = self.center(x)
        box = self.box(x)

        center = center.sigmoid()
        box = torch.exp(box)

        return torch.cat([center, box], 1)
