#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: browser_history_analysis.py
@author: Shengqiang Zhang
@time: 2019/8/5 21:44
@mail: sqzhang77@gmail.com
"""

from platform import system

def system_type():
    sys_str = system()
    print(sys_str)
    if('Windows' in sys_str):
        print('windows')
    elif('Darwin' in sys_str):
        print('macOSX')
    elif('Linux' in sys_str):
        print('linux')
    else:
        print("无法识别你的操作系统类型，请自己设置")


if __name__ == '__main__':
    system_type()



