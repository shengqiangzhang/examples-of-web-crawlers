#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: global_var.py
@author: Shengqiang Zhang
@time: 2019/8/10 01:50
@mail: sqzhang77@gmail.com
"""


def _init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """

    try:
        return _global_dict[key]
    except KeyError:
        return defValue