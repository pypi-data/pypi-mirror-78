#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  test_decorators.py
# @Time      2020/7/21 上午8:49
# @Author    qin_hw
# @Email     1039954093@qq.com

import unittest

from pylantool.decorator import *


class TestDecorators(unittest.TestCase):
    class Person:
        def __init__(self, name, occupation):
            self.name = name
            self.occupation = occupation
            self.call_count2 = 0

        @lazy_property
        def relatives(self):
            # Get all relatives, let's assume that it costs much time.
            relatives = "Many relatives."
            return relatives

        @lazy_property2
        def parents(self):
            self.call_count2 += 1
            return "Father and mother"

    def test_lazy_property(self):
        Jhon = self.Person('Jhon', 'Coder')
        self.assertEqual(Jhon.name, 'Jhon')
        self.assertEqual(Jhon.occupation, 'Coder')
        self.assertEqual(sorted(Jhon.__dict__.items()),
                         [('call_count2', 0), ('name', 'Jhon'), ('occupation', 'Coder')])
        self.assertEqual(Jhon.relatives, 'Many relatives.')
        self.assertTrue('relatives' in Jhon.__dict__ and
                        Jhon.__dict__['relatives'] == 'Many relatives.')
        self.assertEqual(Jhon.call_count2, 0)
        self.assertEqual(Jhon.parents, 'Father and mother')
        self.assertTrue('_lazy__parents' in Jhon.__dict__)
        self.assertTrue(Jhon.__dict__['_lazy__parents'] == 'Father and mother')
        self.assertEqual(Jhon.call_count2, 1)
        self.assertEqual(Jhon.parents, 'Father and mother')
        self.assertEqual(Jhon.call_count2, 1)
