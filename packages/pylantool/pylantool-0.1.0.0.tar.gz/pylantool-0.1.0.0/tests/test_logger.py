#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  test_logger.py
# @Time      2020/7/21 下午12:04
# @Author    qin_hw
# @Email     1039954093@qq.com

import unittest
from pathlib import Path

from pylantool.logger import *
from pylantool.fs import rmPath


class TestLogger(unittest.TestCase):
    def test_logger(self):
        with self.assertRaises(RuntimeError):
            getLogDir()
        with self.assertRaises(RuntimeError):
            getLogger("ts", INFO)

        test_log_dir = Path("./test-logger")
        setLogDir(test_log_dir)
        self.assertEqual(getLogDir(), test_log_dir)
        for i in range(10):
            logger = getLogger("test{}.log".format(i), INFO)
            logger.info("test info message")
            logger.warning("test warning message")
            logger.error("test error message")
            logger.critical("test critical message")
            logger.debug("test debug message")

        for i in range(10):
            logger = getLogger("test{}.log".format(i), INFO)
            logger.info("test info message")
            logger.warning("test warning message")
            logger.error("test error message")
            logger.critical("test critical message")
            logger.debug("test debug message")

        rmPath(test_log_dir, isDir=True)
