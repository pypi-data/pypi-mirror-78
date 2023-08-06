#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  test_fs.py
# @Time      2020/7/21 上午9:10
# @Author    qin_hw
# @Email     1039954093@qq.com

import unittest
from pathlib import Path

from pprint import pprint
from pylantool.fs import *


class TestIO(unittest.TestCase):
    def test_VirtualDirectory(self):
        test_dir = Path("/media/qin_hw/File2/MagneticCoreInsert/left-hand/DATASET/train/left")
        file_paths = list(test_dir.iterdir())

        json_pattern = "*.json"
        json_paths = list(test_dir.glob(json_pattern))
        png_pattern = "*.png"
        png_paths = list(test_dir.glob(png_pattern))
        json_png_pattern = "*[.png, .json]?"
        json_png_paths = list(test_dir.glob(json_png_pattern))

        def assertListEqual(list1, list2):
            self.assertListEqual(list(list1), list2)

        vd1 = VirtualDirectory.fromPaths(list(test_dir.iterdir()))
        assertListEqual(vd1, file_paths)

        assertListEqual(vd1.glob(json_pattern), json_paths)
        assertListEqual(vd1.glob(png_pattern), png_paths)
        assertListEqual(vd1.glob(json_png_pattern), json_png_paths)

        vd2 = vd1 + vd1

        self.assertEqual(len(vd2), 2 * len(vd1))
        pprint(vd2)

    def test_makePath(self):
        path_ = Path("./sdasd/sdasdsa/asdas")
        assert mkPath(path_, isDir=True).is_dir()
        assert mkPath(path_, isDir=False).exists()

        rmPath(path_, isDir=True)
        assert not path_.is_dir()
