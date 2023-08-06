#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  logger.py
# @Time      2020/7/21 上午11:43
# @Author    qin_hw
# @Email     1039954093@qq.com


import logging
from pathlib import Path
from logging import handlers

from .fs import mkPath, rmPath

__all__ = [
    'setLogDir',
    'getLogDir',
    'getLogger',
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL'
]

_LOG_DIR = ""

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def _checkLogDir():
    if not _LOG_DIR:
        raise RuntimeError("LOG_DIR is not set! Call setLogDir method to set it!")


def setLogDir(dir_, overwrite=False):
    dir_ = Path(dir_)

    if overwrite and dir_.is_dir():
        rmPath(dir_, isDir=True)

    global _LOG_DIR
    _LOG_DIR = mkPath(dir_, isDir=True)


def getLogDir():
    _checkLogDir()

    return _LOG_DIR


def getLogger(filename, level, when='D', backupCount=3,
              fmt='%(asctime)s - %(pathname)s[line:%(lineno)d]\n%(levelname)s: %(message)s'):
    _checkLogDir()

    logger = logging.getLogger(filename)
    format_str = logging.Formatter(fmt)
    logger.setLevel(level)

    # set stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(format_str)

    # log file handler
    log_filename = Path(_LOG_DIR) / filename
    if log_filename.suffix != '.log':
        log_filename = log_filename.with_suffix(".log")
    file_handler = handlers.TimedRotatingFileHandler(log_filename.as_posix(),
                                                     when=when,
                                                     backupCount=backupCount,
                                                     encoding='utf-8')
    file_handler.setFormatter(format_str)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
