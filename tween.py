import math
from typing import Callable, Union
import time

def EaseSineInOut(x: float):
    return 1 - math.pow(1 - x, 4)

def EaseLinear(x: float):
    return x


class Tween:
    def __init__(self, func: Callable, start_val: Union[float, int], end_val: Union[float, int], amt_time: float):
        """
        Tween easing helper class

        :param func: Easing function
        :param start_val: Start value
        :param end_val: End value
        :param amt_time: Float amount of time for tween in seconds
        """
        self.func = func
        self.start_val = start_val
        self.end_val = end_val
        self.curr_val = start_val

        self.start_time = time.time()
        self.duration = amt_time

        self.done = False
    def update(self):
        curr_time = time.time() - self.start_time
        if curr_time < self.duration:
            # simulatenous results in end and start val being the same ? ? ?
            self.curr_val = self.start_val + (self.end_val - self.start_val) * self.func(curr_time / self.duration)
        elif not self.done:
            self.done = True
            self.curr_val = self.end_val