#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  _timer.py
# @Time      2020/7/21 上午11:37
# @Author    qin_hw
# @Email     1039954093@qq.com


import time
from functools import wraps
from contextlib import contextmanager

__all__ = [
    'ContextTimer',
    'timeit'
]


@contextmanager
def ContextTimer(blockName=""):
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()

    print(blockName, "cost: {:.8f} s".format(end_time - start_time))


def timeit():
    """Decorator timer, time the decorated function run-time"""

    def _TimerDecorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            ret = func(*args, **kwargs)
            end_time = time.perf_counter()

            print("{}.{} cost {:.8f} s".format(func.__module__, func.__name__,
                                               end_time - start_time))
            return ret

        return wrapper

    return _TimerDecorator


if __name__ == '__main__':
    with ContextTimer("Test"):
        time.sleep(1)
