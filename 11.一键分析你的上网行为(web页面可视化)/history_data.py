#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: history_data.py
@author: Shengqiang Zhang
@time: 2019/8/5 21:44
@mail: sqzhang77@gmail.com
"""

import sqlite3


# 查询数据库内容
def query_sqlite_db(history_db, query):

    # 查询sqlite数据库
    # 注意，History是一个文件，没有后缀名。它不是一个目录。
    conn = sqlite3.connect(history_db)
    cursor = conn.cursor()

    # 使用sqlite查看软件，可清晰看到表visits的字段url=表urls的字段id
    # 连接表urls和visits，并获取指定数据
    select_statement = query

    # 执行数据库查询语句
    cursor.execute(select_statement)

    # 获取数据，数据格式为元组(tuple)
    results = cursor.fetchall()

    # 关闭
    cursor.close()
    conn.close()

    return results




# 获取排序后的历史数据
def get_history_data(history_file_path):

    try:

        # 获取数据库内容
        # 数据格式为元组(tuple)
        select_statement = "SELECT urls.id, urls.url, urls.title, urls.last_visit_time, urls.visit_count, visits.visit_time, visits.from_visit, visits.transition, visits.visit_duration FROM urls, visits WHERE urls.id = visits.url;"
        result = query_sqlite_db(history_file_path, select_statement)

        # 将结果按第1个元素进行排序
        # sort和sorted内建函数会优先排序第1个元素，然后再排序第2个元素，依此类推
        result_sort = sorted(result, key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))

        # 返回排序后的数据
        return result_sort
    except:
        # print('读取出错!')
        return 'error'



# 获取 搜索关键词 数据
def get_search_word(history_file_path):

    try:

        # 获取数据库内容
        # 数据格式为元组(tuple)
        select_statement = "SELECT keyword_search_terms.url_id, keyword_search_terms.term, urls.url, urls.last_visit_time from keyword_search_terms LEFT JOIN urls on keyword_search_terms.url_id=urls.id;"
        result = query_sqlite_db(history_file_path, select_statement)

        # 将结果按第1个元素(下标为0)进行升序排序
        result_sort = sorted(result, key=lambda x: (x[0]))

        # 返回排序后的数据
        return result_sort
    except:
        # print('读取出错!')
        return 'error'