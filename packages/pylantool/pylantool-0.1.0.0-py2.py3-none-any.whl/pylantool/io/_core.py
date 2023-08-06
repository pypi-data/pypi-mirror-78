#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  _core.py
# @Time      2020/7/21 上午11:28
# @Author    qin_hw
# @Email     1039954093@qq.com

# !/usr/bin/env python
# -*- coding:utf-8 -*-

# copy from http://192.168.16.33/huang_kh/toolbox/-/blob/master/toolbox/fileinterface/core.py


import os
import sys
import json
import pickle as pk

__all__ = [
    'loadPk',
    'dumpPk',
    'loadJson',
    'dumpJson',
    'PK_HIGHEST_PROTOCOL',
    'PK_DEFAULT_PROTOCOL',
    'PK_PROTOCOL_0',
    'PK_PROTOCOL_1',
    'PK_PROTOCOL_2',
    'PK_PROTOCOL_3',
    'PK_PROTOCOL_4',
]

PK_HIGHEST_PROTOCOL = pk.HIGHEST_PROTOCOL
if hasattr(pk, "DEFAULT_PROTOCOL"):
    PK_DEFAULT_PROTOCOL = getattr(pk, "DEFAULT_PROTOCOL")
else:
    PK_DEFAULT_PROTOCOL = None
PK_PROTOCOL_0 = 0
PK_PROTOCOL_1 = 1
PK_PROTOCOL_2 = 2
PK_PROTOCOL_3 = 3
PK_PROTOCOL_4 = 4


def loadPk(fileName, method='rb'):
    """
    Read a pickled object representation from the open file.
    Return the reconstituted object hierarchy specified in the file.
    """
    if method == "r":
        method = "rb"
        sys.stderr.write("loadPk: using 'rb' instead of 'r'\n")
    with open(fileName, method) as f:
        return pk.load(f)


def dumpPk(data, fileName, method='wb', protocol=PK_DEFAULT_PROTOCOL, safeMode=False):
    """
    Write a pickled representation of obj to the open file.
    """
    if method == "w":
        method = "wb"
        sys.stderr.write("dumpPk: using 'wb' instead of 'w'\n")

    if safeMode:
        temp_file_name = fileName + '_temp'
    else:
        temp_file_name = fileName

    with open(temp_file_name, method) as f:
        pk.dump(obj=data, file=f, protocol=protocol)
        if safeMode:
            f.flush()
            os.fsync(f.fileno())

    if safeMode:
        os.rename(temp_file_name, fileName)


def loadJson(filename):
    with open(filename) as f:
        return json.load(f)


def dumpJson(filename, data):
    with open(filename, mode='w') as f:
        json.dump(data, f)
