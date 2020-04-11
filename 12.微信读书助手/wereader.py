#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: wereader.py
@author: Shengqiang Zhang
@time: 2020/4/11 16:04
@mail: sqzhang77@gmail.com
"""


import requests
import urllib3
# 禁用安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_notebooklist(headers):
    """获取笔记书单"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = requests.get(url,headers=headers,verify=False)

    if r.ok:
        data = r.json()
        print(data)
    else:
        data = r.json()
        print(data)
        # raise Exception(r.text)
    # books = []
    # for b in data['books']:
    #     book = b['book']
    #     b = Book(book['bookId'],book['title'],book['author'],book['cover'],book['category'])
    #     books.append(b)
    # books.sort(key=itemgetter(-1))
    # return books


def login_success(headers):
    """判断是否登录成功"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = requests.get(url,headers=headers,verify=False)

    if r.ok:
        return True
    else:
        return False



