"""
Box 检测框类
"""

import cv2

__all__ = ['draw_boxes', 'nms']


def draw_boxes(im, boxes, color=(0, 255, 0)):
    """
    在图上画框
    :param im: ndarray 图片
    :param boxes: box 数组 box -> (x1, y1, x2, y2)
    :param color: 框颜色 (r, g, b), 默认绿色
    :return:
    """
    im = im.copy()
    for box in boxes:
        x1, y1, x2, y2 = tuple(map(int, box))
        im = cv2.rectangle(im, (x1, y1), (x2, y2), color, 2, 16)
    return im


def nms(boxes, threshold=0.7):
    """
    非极大值抑制
    :param boxes: 如果是已经排序好的的, 输入 (x0, y0, x1, y1) 否则输入 (x0, y0, x1, y1, confidence)
    :param threshold: 阈值, 重叠部分大于阈值将会被忽略
    :return: nms 后的框
    """

    if len(boxes[0]) == 5:  # With Confidence
        boxes = sorted(boxes, key=lambda x: -x[-1])
        boxes = list(map(lambda x: x[:4], boxes))

    keep = []
    for x01, y01, x02, y02 in boxes:
        is_keep = True
        for x11, y11, x12, y12 in keep:
            x = min(x02, x12) - max(x01, x11)
            y = min(y02, y12) - max(y01, y11)
            if x < 0 or y < 0:
                continue
            if x * y >= (y02 - y01) * (x02 - x01) * threshold:
                is_keep = False
        if is_keep:
            keep.append((x01, y01, x02, y02))
    return keep

