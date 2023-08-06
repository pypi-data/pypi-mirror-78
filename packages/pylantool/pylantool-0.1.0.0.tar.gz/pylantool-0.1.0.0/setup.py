# -*- coding: utf-8 -*-


__date__ = '2020-06-24'
__author__ = 'qin_hw'
__author_email__ = '1039954093@qq.com'

from setuptools import find_packages, setup

setup(
    name="pylantool",
    version="0.1.0.0",
    url="https://gitee.com/mysticalwing/pylantool",
    description="A collection of functions common used in python programing",

    author="qin_hw",
    author_email="1039954093@qq.com",

    classifiers=[
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[],
)
