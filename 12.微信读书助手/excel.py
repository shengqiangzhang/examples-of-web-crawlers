#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: excel.py
@author: Shengqiang Zhang
@time: 2020/4/11 21:14
@mail: sqzhang77@gmail.com
"""


import xlrd
import xlwt
from xlutils.copy import copy

if __name__ == '__main__':
    print('hello world!')


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
        print("xls格式表格【追加】写入数据成功！")


    def read_excel_xls(path):
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        for i in range(0, worksheet.nrows):
            for j in range(0, worksheet.ncols):
                print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
            print()


    book_name_xls = '我的书架.xls'

    sheet_name_finish_read = '所有的书籍'
    sheet_name_recent_read = '最近阅读的书籍'
    sheet_name_all = '已读完的书籍'

    value_title = [["ID", "标题", "作者", "封面", "简介", "所属目录"], ]

    value1 = [["张三", "男", "19", "杭州", "研发工程师", "1"],
              ["李四", "男", "22", "北京", "医生", "1"],
              ["王五", "女", "33", "珠海", "出租车司机", "1"], ]

    value2 = [["Tom", "男", "21", "西安", "测试工程师", "1"],
              ["Jones", "女", "34", "上海", "产品经理", "1"],
              ["Cat", "女", "56", "上海", "教师", "1"], ]

    write_excel_xls(book_name_xls, [sheet_name_finish_read, sheet_name_recent_read, sheet_name_all], value_title)

    write_excel_xls_append(book_name_xls, sheet_name_finish_read, value1)
    write_excel_xls_append(book_name_xls, sheet_name_recent_read, value2)
    #read_excel_xls(book_name_xls)