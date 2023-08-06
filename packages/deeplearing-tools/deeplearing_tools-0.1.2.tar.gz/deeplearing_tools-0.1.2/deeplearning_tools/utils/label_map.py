__all__ = ['parse_label_map_c2i', 'parse_label_map_i2c']


def parse_label_map_c2i(label_map):
    """
    解析 LabelMap 为 Char -> Index 的字典
    :param label_map: 原始码表
    :return: Dict
    """
    if isinstance(label_map, dict):
        return label_map
    elif isinstance(label_map, list):
        return dict(zip(label_map, list(range(0, len(label_map)))))
    elif isinstance(label_map, str):
        return parse_label_map_c2i([i for i in label_map])
    else:
        raise TypeError("LabelMap must be dict list or str")


def parse_label_map_i2c(label_map):
    """
    解析 LabelMap 为 Index -> Char 的字典
    :param label_map: 原始码表
    :return: Dict
    """
    if isinstance(label_map, dict):
        return label_map
    elif isinstance(label_map, list):
        return dict(zip(list(range(0, len(label_map))), label_map))
    elif isinstance(label_map, str):
        return parse_label_map_i2c([i for i in label_map])
    else:
        raise TypeError("LabelMap must be dict list or str")



