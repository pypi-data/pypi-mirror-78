#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  _core.py
# @Time      2020/7/21 上午10:49
# @Author    qin_hw
# @Email     1039954093@qq.com

import os
import shutil
from pathlib import Path

__all__ = [
    'mkPath',
    'rmPath',
    'ensureSuffix',
]


def mkPath(path_, isDir: bool):
    path_ = Path(path_)

    if isDir and not path_.is_dir():
        os.makedirs(path_)
        assert path_.is_dir()
    else:
        path_.touch()

    return path_


def rmPath(path_, isDir: bool):
    path_ = Path(path_)
    if isDir and path_.is_dir():
        shutil.rmtree(path_)
    elif path_.is_file():
        os.remove(path_)


def ensureSuffix(path_, suffix: str):
    path_ = Path(path_)

    if path_.suffix != suffix:
        path_ = path_.with_suffix(path_.suffix + suffix)

    return path_
