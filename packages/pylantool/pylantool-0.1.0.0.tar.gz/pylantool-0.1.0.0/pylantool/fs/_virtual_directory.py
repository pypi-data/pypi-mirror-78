#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  _virtual_directory.py
# @Time      2020/7/21 上午9:02
# @Author    qin_hw
# @Email     1039954093@qq.com

# -*- coding: utf-8 -*-


__date__ = '2020-07-13'
__author__ = 'qin_hw'
__author_email__ = '1039954093@qq.com'

from pathlib import Path
from typing import Generator, List
from collections import Collection

__all__ = [
    'VirtualDirectory',
]


class VirtualDirectory(Collection):
    def __init__(self, paths):
        self._paths: List[Path] = paths

    @classmethod
    def fromPaths(cls, paths):
        file_paths = []
        for path_ in paths:
            path_ = Path(path_)
            if not path_.exists():
                continue

            file_paths += list(path_.iterdir()) if path_.is_dir() else [path_]

        return cls(file_paths)

    def glob(self, pattern: str) -> Generator[Path, None, None]:
        for path_ in self._paths:
            if path_.match(pattern):
                yield path_

    def add(self, path_: Path, checkExists=True):
        path_ = Path(path_)

        if checkExists and not path_.exists():
            return

        self._paths.append(path_)

    def __len__(self):
        return len(self._paths)

    def __add__(self, other: 'VirtualDirectory'):
        return self.__class__.fromPaths(self._paths + other._paths)

    def __iadd__(self, other: 'VirtualDirectory'):
        self._paths.extend(other._paths)

    def __iter__(self):
        return iter(self._paths)

    def __contains__(self, path_):
        return path_ in self._paths

    def __repr__(self):
        return "[{}]".format(",\n".join((str(path) for path in self)))
