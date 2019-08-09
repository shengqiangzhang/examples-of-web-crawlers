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
    def update_player_statistics_value(available_options):
        # print(available_options)
        return available_options[0]['value']



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
            data = get_history_data()
            history_data = global_var.set_value('history_data', data)
            # for i in history_data:
            #     print(i)

            if (history_data != 'error'):
                # 找到
                return 1
            else:
                # 没找到
                return 0
        else:
            return 0