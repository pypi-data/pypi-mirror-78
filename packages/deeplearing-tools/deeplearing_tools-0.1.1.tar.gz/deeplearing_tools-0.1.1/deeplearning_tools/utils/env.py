import os
from importlib import import_module

__all__ = ['__TORCH_AVAILABLE__', '__NUMPY_AVAILABLE__']


def check_module(name):
    try:
        import_module(name)
        return True
    except ImportError:
        return False


__TORCH_AVAILABLE__ = check_module('torch')
if "DISABLE_TORCH" in os.environ and os.environ["DISABLE_TORCH"]:
    __TORCH_AVAILABLE__ = False

__NUMPY_AVAILABLE__ = check_module('numpy')
assert __NUMPY_AVAILABLE__  # 必须有 Numpy
