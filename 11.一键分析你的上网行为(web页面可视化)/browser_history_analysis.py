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
import os
import shutil
import sqlite3





# 获取历史记录文件所在的路径
def get_history_file_path():

    # 获取操作系统信息
    sys_str = system()

    # 历史记录文件所在的路径
    file_path = ""

    if('Windows' in sys_str):
        # print('Windows')
        home = os.environ['HOMEPATH']
        file_path = ""
    elif('Darwin' in sys_str):
        # print('macOSX')
        home = os.environ['HOME']
        file_path = home + "/Library/Application Support/Google/Chrome/Default/History"
    elif('Linux' in sys_str):
        # print('Linux')
        home = os.environ['HOME']
        file_path = ""
    else:
        # print('unknown')
        file_path = ""

    print(file_path)
    return file_path




# 查询数据库内容
def query_sqlite_db(history_db):

    # 查询sqlite数据库
    # 注意，History是一个文件，没有后缀名。它不是一个目录。
    c = sqlite3.connect(history_db)
    cursor = c.cursor()

    # 使用sqlite查看软件，可清晰看到表visits的字段url=表urls的字段id
    # 连接表urls和visits，并获取指定数据
    select_statement = "SELECT urls.id, urls.url, urls.title, urls.last_visit_time, urls.visit_count, visits.visit_time, visits.from_visit, visits.transition, visits.visit_duration FROM urls, visits WHERE urls.id = visits.url;"

    # 执行数据库查询语句
    cursor.execute(select_statement)

    # 获取数据，数据格式为元组(tuple)
    results = cursor.fetchall()

    return results




# 获取排序后的历史数据
def get_history_data():
    # 获取历史记录文件所在的路径
    # 根据不同操作系统自动获取对应的历史记录文件
    history_file_path = get_history_file_path()

    # 判断该历史文件是否存在
    # 若不存在，则需要手动将历史记录文件复制到当前目录下
    if not os.path.exists(history_file_path):
        print('历史记录文件不存在!')
        return 'error'


    # 复制(拷贝)历史记录文件到当前目录下
    # 因为历史记录其实是一个sqlite数据库文件，sqlite是单线程，浏览器在运行时，数据库是默认锁住的
    # 注意，History是一个文件，没有后缀名。它不是一个目录。
    try:
        shutil.copyfile(history_file_path, './History')

        # 获取数据库内容
        # 数据格式为元组(tuple)
        result = query_sqlite_db('./History')

        # 将结果按第1个元素进行排序
        # sort和sorted内建函数会优先排序第1个元素，然后再排序第2个元素，依此类推
        result_sort = sorted(result, key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))

        # 返回排序后的数据
        return result_sort
    except:
        print('复制历史文件出错!')
        return 'error'


