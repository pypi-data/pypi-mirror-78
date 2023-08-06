import math
import torch
from lengyue_dl.dataset.detection import DetectionDataset


def gaussian_2d(shape, sigma=1):
    m, n = [(ss - 1.) / 2. for ss in shape]
    m, n = int(m), int(n)
    h = torch.zeros((m * 2 + 1, n * 2 + 1), dtype=torch.float32)
    for y in range(-m, m + 1):
        for x in range(-n, n + 1):
            h[x + n, y + m] = 2.71828182846 ** (-(x * x + y * y) / (2 * sigma * sigma))
    h[h < torch.finfo(h.dtype).eps * h.max()] = 0
    return h


def draw_gaussian(heatmap, center, radius, k=1):
    radius = math.ceil(radius)
    diameter = 2 * radius + 1
    gaussian = gaussian_2d((diameter, diameter), sigma=diameter / 6)

    x, y = int(center[0]), int(center[1])

    height, width = heatmap.shape[0:2]

    left, right = min(x, radius), min(width - x, radius + 1)
    top, bottom = min(y, radius), min(height - y, radius + 1)

    masked_heatmap = heatmap[y - top:y + bottom, x - left:x + right]
    masked_gaussian = gaussian[radius - top:radius + bottom, radius - left:radius + right]
    if min(masked_gaussian.shape) > 0 and min(masked_heatmap.shape) > 0:  # TODO debug
        torch.max(masked_heatmap, masked_gaussian * k, out=masked_heatmap)
    return heatmap

# x0,y0,x1,y1
class CenterNetDataset(DetectionDataset):

    def __getitem__(self, item):
        image, boxes = super().__getitem__(item)
        raw_h, raw_w = image.shape[:2] #torch.Size([384, 344, 3])
        image = self.transform(image)  # 1, H, W
        new_h, new_w = image.shape[1:]  #torch.Size([3, 256, 256])
        stride = 4
        hm_height = image.shape[1] // stride
        hm_width = image.shape[2] // stride
        hm = torch.zeros((1, hm_height, hm_width), dtype=torch.float32)
        xywh = torch.zeros((4, hm_height, hm_width), dtype=torch.float32)
        xywh_mask = torch.zeros((4, hm_height, hm_width), dtype=torch.float32)

        for x, y, r, b in boxes:
            x = x / raw_w * new_w
            y = y / raw_h * new_h
            r = r / raw_w * new_w
            b = b / raw_h * new_h
            w = r - x + 1
            h = b - y + 1

            radius = (w + h) * 0.5 / 16
            real_cx = (x + r) * 0.5 / stride
            real_cy = (y + b) * 0.5 / stride
            icx = int(real_cx)
            icy = int(real_cy)

            draw_gaussian(hm[0], (icx, icy), radius)

            range_expand = 2
            for cx in range(icx - range_expand, icx + range_expand + 1):
                for cy in range(icy - range_expand, icy + range_expand + 1):
                    dw = (w / stride)
                    dh = (h / stride)
                    left = real_cx - dw / 2.
                    top = real_cy - dh / 2.
                    right = real_cx + dw / 2.
                    bottom = real_cy + dh / 2.

                    xywh[0:4, cy, cx] = torch.FloatTensor([cx - left, cy - top, right - cx, bottom - cy])
                    xywh_mask[0:4, cy, cx] = 1

        return image, hm, xywh, xywh_mask
