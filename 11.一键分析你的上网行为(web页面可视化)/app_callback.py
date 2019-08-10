#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app_callback.py
@author: Shengqiang Zhang
@time: 2019/8/10 01:15
@mail: sqzhang77@gmail.com
"""

import dash

from app_configuration import app
from app_plot import *

from history_data import *
import random
import base64
import time
from os.path import exists
from os import makedirs



# 回调，用于更新web页面数据
# dash框架是前后端不分离的，所以仅仅适用于简单页面部署，复杂页面不推荐使用dash
def app_callback_function():

    # 页面访问频率排名
    @app.callback(
        dash.dependencies.Output('graph_website_count_rank', 'figure'),
        [
            dash.dependencies.Input('input_website_count_rank', 'value'),
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(value, store_memory_history_data):

        # 正确获取到历史记录文件
        if store_memory_history_data:
            history_data = store_memory_history_data['history_data']
            figure = plot_bar_website_count_rank(value, history_data)
            return figure
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")




    # 每日访问次数
    @app.callback(
        dash.dependencies.Output('graph_day_count_rank', 'figure'),
        [
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(store_memory_history_data):


        # 正确获取到历史记录文件
        if store_memory_history_data:
            history_data = store_memory_history_data['history_data']
            figure = plot_scatter_website_count_rank(history_data)
            return figure
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")





    # 访问次数最多的URL
    @app.callback(
        dash.dependencies.Output('table_url_count_rank', 'data'),
        [
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(store_memory_history_data):

        # 正确获取到历史记录文件
        if store_memory_history_data:
            history_data = store_memory_history_data['history_data']
            table_data = table_data_url_count_rank(history_data)
            return table_data
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")





    # 页面访问停留时间排名
    @app.callback(
        dash.dependencies.Output('table_url_time_rank', 'data'),
        [
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(store_memory_history_data):

        # 正确获取到历史记录文件
        if store_memory_history_data:
            history_data = store_memory_history_data['history_data']
            table_data = table_data_url_time_rank(history_data)
            return table_data
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")





    # 某日不同时刻访问次数
    @app.callback(
        dash.dependencies.Output('dropdown_time_1', 'options'),
        [
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(store_memory_history_data):

        # 正确获取到历史记录文件
        if store_memory_history_data:
            history_data = store_memory_history_data['history_data']
            result_ist = get_history_date_time(history_data)
            result_options = []

            for data in result_ist:
                result_options.append({'label': data, 'value': data})

            return result_options
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")






    # 自动选择dropdown的第一个选option
    @app.callback(
        dash.dependencies.Output('dropdown_time_1', 'value'),
        [
            dash.dependencies.Input('dropdown_time_1', 'options')
        ]
    )
    def update(available_options):
        # print(available_options)
        if(available_options):
            return available_options[0]['value']
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")






    # dropdown_time_1的value发生改变时的回调
    @app.callback(
        dash.dependencies.Output('graph_day_diff_time_count', 'figure'),
        [
            dash.dependencies.Input('dropdown_time_1', 'value'),
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(date_time_value, store_memory_history_data):
        if(date_time_value):
            if store_memory_history_data:
                history_data = store_memory_history_data['history_data']
                figure = plot_scatter_website_diff_time(date_time_value, history_data)
                return figure
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")


        # 取消更新页面数据
        raise dash.exceptions.PreventUpdate("cancel the callback")








    # 搜索关键词排名
    @app.callback(
        [
            dash.dependencies.Output('graph_search_word_count_rank', 'figure'),
            dash.dependencies.Output('graph_search_engine_count_rank', 'figure')
        ],

        [
            dash.dependencies.Input('store_memory_history_data', 'data')
        ]
    )
    def update(store_memory_history_data):

        # 正确获取到历史记录文件
        if (store_memory_history_data is not None):
            search_word = store_memory_history_data['search_word']
            figure_1, figure_2 = plot_bar_search_word_count_rank(search_word)
            return figure_1, figure_2
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")



    # 上传文件回调
    @app.callback(

        dash.dependencies.Output('store_memory_history_data', 'data'),
        [
            dash.dependencies.Input('dcc_upload_file', 'contents')
        ]
    )
    def update(contents):

        if contents is not None:

            # 接收base64编码的数据
            content_type, content_string = contents.split(',')

            # 将客户端上传的文件进行base64解码
            decoded = base64.b64decode(content_string)

            # 为客户端上传的文件添加后缀，防止文件重复覆盖
            # 以下方式确保文件名不重复
            suffix = [str(random.randint(0,100)) for i in range(10)]
            suffix = "".join(suffix)
            suffix = suffix + str(int(time.time()))

            # 最终的文件名
            file_name = 'History_' + suffix
            # print(file_name)

            # 创建存放文件的目录
            if (not (exists('data'))):
                makedirs('data')

            # 欲写入的文件路径
            path = 'data' + '/' + file_name

            # 写入本地磁盘文件
            with open(file=path, mode='wb+') as f:
                f.write(decoded)


            # 使用sqlite读取本地磁盘文件
            # 获取历史记录数据
            history_data = get_history_data(path)
            # for i in history_data:
            #     print(i)

            # 获取搜索关键词数据
            search_word = get_search_word(path)
            # for i in search_word:
            #     print(i)

            # 判断读取到的数据是否正确
            if (history_data != 'error'):
                # 找到
                date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print('新接收到一条客户端的数据, 数据正确, 时间:{}'.format(date_time))
                store_data = {'history_data': history_data, 'search_word': search_word}
                return store_data
            else:
                # 没找到
                date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print('新接收到一条客户端的数据, 数据错误, 时间:{}'.format(date_time))
                return  None

        return None


