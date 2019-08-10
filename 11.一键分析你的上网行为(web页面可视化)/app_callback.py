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
import global_var



# 回调，用于更新web页面数据
# dash框架是前后端不分离的，所以仅仅适用于简单页面部署，复杂页面不推荐使用dash
def app_callback_function():

    # 页面访问频率排名
    @app.callback(
        dash.dependencies.Output('graph_website_count_rank', 'figure'),
        [
            dash.dependencies.Input('input_website_count_rank', 'value'),
            dash.dependencies.Input('auto_find_text_flag', 'value')
        ]
    )
    def update(value, auto_find_text_flag):

        # 跨文件全局变量
        history_data = global_var.get_value('history_data')

        # 正确获取到历史记录文件
        if (history_data != 'error' and auto_find_text_flag == 1):
            figure = plot_bar_website_count_rank(value)
            return figure
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")




    # 每日访问次数
    @app.callback(
        dash.dependencies.Output('graph_day_count_rank', 'figure'),
        [
            dash.dependencies.Input('auto_find_text_flag', 'value')
        ]
    )
    def update(auto_find_text_flag):

        # 跨文件全局变量
        history_data = global_var.get_value('history_data')

        # 正确获取到历史记录文件
        if (history_data != 'error' and auto_find_text_flag == 1):
            figure = plot_scatter_website_count_rank()
            return figure
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")





    # 访问次数最多的URL
    @app.callback(
        dash.dependencies.Output('table_url_count_rank', 'data'),
        [
            dash.dependencies.Input('auto_find_text_flag', 'value')
        ]
    )
    def update(auto_find_text_flag):

        # 跨文件全局变量
        history_data = global_var.get_value('history_data')

        # 正确获取到历史记录文件
        if (history_data != 'error' and auto_find_text_flag == 1):
            table_data = table_data_url_count_rank()
            return table_data
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")





    # 页面访问停留时间排名
    @app.callback(
        dash.dependencies.Output('table_url_time_rank', 'data'),
        [
            dash.dependencies.Input('auto_find_text_flag', 'value')
        ]
    )
    def update(auto_find_text_flag):

        # 跨文件全局变量
        history_data = global_var.get_value('history_data')

        # 正确获取到历史记录文件
        if (history_data != 'error' and auto_find_text_flag == 1):
            table_data = table_data_url_time_rank()
            return table_data
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")





    # 某日不同时刻访问次数
    @app.callback(
        dash.dependencies.Output('dropdown_time_1', 'options'),
        [
            dash.dependencies.Input('auto_find_text_flag', 'value')
        ]
    )
    def update(auto_find_text_flag):

        # 跨文件全局变量
        history_data = global_var.get_value('history_data')

        # 正确获取到历史记录文件
        if (history_data != 'error' and auto_find_text_flag == 1):
            result_ist = get_history_date_time()
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
            dash.dependencies.Input('dropdown_time_1', 'value')
        ]
    )
    def update(date_time_value):
        if(date_time_value):
            figure = plot_scatter_website_diff_time(date_time_value)
            return figure
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")








    # 搜索关键词排名
    @app.callback(
        [
            dash.dependencies.Output('graph_search_word_count_rank', 'figure'),
            dash.dependencies.Output('graph_search_engine_count_rank', 'figure')
        ],

        [
            dash.dependencies.Input('auto_find_text_flag', 'value')
        ]
    )
    def update(auto_find_text_flag):

        # 跨文件全局变量
        search_word = global_var.get_value('search_word')

        # 正确获取到历史记录文件
        if (search_word != 'error' and auto_find_text_flag == 1):
            figure_1, figure_2 = plot_bar_search_word_count_rank()
            return figure_1, figure_2
        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")







    # 判断是否自动寻找到历史记录文件
    @app.callback(
        dash.dependencies.Output('auto_find_text_flag', 'value'),
        [
            dash.dependencies.Input('first_load_web_page', 'value')
        ]
    )
    def update(value):

        # value对象不为null
        if (value is not None):

            # 获取历史记录数据，跨文件全局变量
            history_data = get_history_data()
            global_var.set_value('history_data', history_data)
            # for i in history_data:
            #     print(i)

            # 获取搜索关键词数据，跨文件全局变量
            search_word = get_search_word()
            global_var.set_value('search_word', search_word)
            # for i in search_word:
            #     print(i)


            if (history_data != 'error'):
                # 找到
                return 1
            else:
                # 没找到
                return 0
        else:
            return 0