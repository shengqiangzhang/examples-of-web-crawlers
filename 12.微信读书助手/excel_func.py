#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: excel_func.py
@author: Shengqiang Zhang
@time: 2020/4/11 21:14
@mail: sqzhang77@gmail.com
"""


import xlrd
import xlwt
from xlutils.copy import copy


def write_excel_xls(path, sheet_name_list, value):
    # 新建一个工作簿
    workbook = xlwt.Workbook()

    # 获取需要写入数据的行数
    index = len(value)

    for sheet_name in sheet_name_list:

        # 在工作簿中新建一个表格
        sheet = workbook.add_sheet(sheet_name)

        # 往这个工作簿的表格中写入数据
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.write(i, j, value[i][j])

    # 保存工作簿
    workbook.save(path)


def write_excel_xls_append(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    worksheet = workbook.sheet_by_name(sheet_name)  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(sheet_name)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("{}【追加】写入【{}】数据成功！".format(path, sheet_name))


