from time import perf_counter

__all__ = ['Timer']


class Timer:
    def __init__(self):
        self.begin = 0
        self.restart()

    def restart(self):
        self.begin = perf_counter()
        return self

    def cost(self):
        """
        取从 Start 开始的运行时间
        :return:
        """
        return perf_counter() - self.begin

