#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app_plot.py
@author: Shengqiang Zhang
@time: 2019/8/10 02:03
@mail: sqzhang77@gmail.com
"""


import plotly.graph_objs as go
import time


# 对url地址进行简化
def url_simplification(url):
    tmp_url = url

    try:
        url = url.split('//')
        url = url[1].split('/', 1)
        url = url[0].replace("www.", "")
        return url

    except IndexError:
        # print('特殊的url')
        return tmp_url


# 获取字典的前k个最大的子集合，按value
def get_top_k_from_dict(origin_dict, k):
    origin_dict_len = len(origin_dict)
    n = k

    if(n > origin_dict_len):
        n = origin_dict_len

    new_data = sorted(origin_dict.items(), key=lambda item: item[1], reverse=True)
    new_data = new_data[:n]

    new_dict = {}
    for l in new_data:
        new_dict[l[0]] = l[1]

    return new_dict


# 获取字典的前k个最大的子集合，按value中的第1个值
def get_top_k_from_dict_value_1(origin_dict, k):
    origin_dict_len = len(origin_dict)
    n = k

    if(n > origin_dict_len):
        n = origin_dict_len

    new_data = sorted(origin_dict.items(), key=lambda item: item[1][0], reverse=True)
    new_data = new_data[:n]

    new_dict = {}
    for l in new_data:
        new_dict[l[0]] = l[1]

    return new_dict


# 对时间字典进行升序排序
def sort_time_dict(origin_dict):
    new_data = sorted(origin_dict.items(), key=lambda item: time.mktime(time.strptime(item[0], "%Y-%m-%d")), reverse=False)
    new_dict = {}
    for l in new_data:
        new_dict[l[0]] = l[1]

    return new_dict


# 转化为数字
def convert_to_number(value):
    try:
        x = int(value)
    except TypeError:
        return 0
    except ValueError:
        return 0
    except Exception as e:
        return 0
    else:
        return x









# 绘制 页面访问频率排名 柱状图
def plot_bar_website_count_rank(value, history_data):

    # 频率字典
    dict_data = {}

    # 对历史记录文件进行遍历
    for data in history_data:
        url = data[1]
        # 简化url
        key = url_simplification(url)

        if (key in dict_data.keys()):
            dict_data[key] += 1
        else:
            dict_data[key] = 0

    # 筛选出前k个频率最高的数据
    k = convert_to_number(value)
    top_10_dict = get_top_k_from_dict(dict_data, k)

    figure = go.Figure(
        data=[
            go.Bar(
                x=[i for i in top_10_dict.keys()],
                y=[i for i in top_10_dict.values()],
                name='bar',
                marker=go.bar.Marker(
                    color='rgb(55, 83, 109)'
                )
            )
        ],
        layout=go.Layout(
            showlegend=False,
            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='网站'),
            yaxis=dict(title='次数')
        )
    )


    return figure








# 绘制 搜索关键词排名柱状图 和 搜索引擎使用情况饼图
def plot_bar_search_word_count_rank(search_word):


    # 频率字典
    dict_data = {}

    # 对搜索关键词数据进行遍历
    for data in search_word:
        search_item = data[1]
        key = search_item

        if (key in dict_data.keys()):
            dict_data[key][0] += 1
        else:
            url_link = data[2]
            url_visit_time = data[3]
            dict_data[key] = [1, url_link, url_visit_time]


    # 筛选出前10个频率最高的数据
    top_10_dict = get_top_k_from_dict_value_1(dict_data, 10)
    # print(top_10_dict)

    # 绘制搜索关键词柱状图
    figure_1 = go.Figure(
        data=[
            go.Bar(
                x=[key for key in top_10_dict.keys()],
                y=[value[0] for value in top_10_dict.values()],
                name='bar',
                marker=go.bar.Marker(
                    color='rgb(55, 83, 109)'
                )
            )
        ],
        layout=go.Layout(
            showlegend=False,
            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='关键词'),
            yaxis=dict(title='次数')
        )
    )






    search_engine_list = ['www.google.com', 'www.bing.com', 'www.yahoo.com', 'www.baidu.com', 'www.sogou.com', 'www.so.com']
    search_engine_value = [0, 0, 0, 0, 0, 0]
    for key, value in dict_data.items():
        for i in range(len(search_engine_list)):
            if search_engine_list[i] in value[1]:
                search_engine_value[i] += 1
                break



    # 绘制搜索引擎使用情况饼图
    figure_2 = go.Figure(
        data=[
            go.Pie(
                labels=search_engine_list,
                values=search_engine_value,
                hole=.3
            )
        ]
    )


    return figure_1, figure_2





# 绘制 每日访问次数 散点图
def plot_scatter_website_count_rank(history_data):

    # 频率字典
    dict_data = {}

    # 对历史记录文件进行遍历
    for data in history_data:
        date_time = data[5]

        # 由于Chrome浏览器在sqlite中存储的时间是以1601-01-01 00:00:00 为起始时间点的微妙计数
        # 与Unix时间戳存在时间间隔，所以需要转换
        unix_time_samp = (date_time / 1000000) - 11644473600

        # 中国以北京时间为准，北京时间为UTC+8小时，8小时=28800秒
        unix_time_samp += 28800

        key = time.strftime("%Y-%m-%d", time.gmtime(unix_time_samp))


        if (key in dict_data.keys()):
            dict_data[key] += 1
        else:
            dict_data[key] = 0

    # 对字典按key进行时间排序
    dict_sort_data = sort_time_dict(dict_data)
    # print(dict_sort_data)
    max_value_dict = max([i for i in dict_sort_data.values()])

    figure = go.Figure(
        data=[
            go.Scatter(
                x=[i for i in dict_sort_data.keys()],
                y=[i for i in dict_sort_data.values()],
                name='lines+markers',
                mode='lines+markers',
                marker_color='rgba(55, 83, 109, .8)',
                marker=dict(size=[(i/max_value_dict)*30 for i in dict_sort_data.values()]),
                fill='tozeroy'
            )
        ],

        layout=go.Layout(
            showlegend=False,
            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='时间'),
            yaxis=dict(title='次数')
        )
    )

    return figure




# 返回 访问次数最多的URL 的数据
def table_data_url_count_rank(history_data):

    # 频率字典
    dict_data = {}

    # 对历史记录文件进行遍历
    for data in history_data:
        url_id = data[0]
        key = url_id

        if (key in dict_data.keys()):
            # 存储url访问次数
            dict_data[key][0] += 1
            # 存储url地址
            dict_data[key][1] = data[1]
            # 存储url标题
            dict_data[key][2] = data[2]

        else:
            dict_data[key] = [0, '', '']



    # 筛选出前k=10个频率最高的数据
    top_k_dict = get_top_k_from_dict_value_1(dict_data, 100)
    # print(top_k_dict)

    # 返回的table data数据
    table_data = []

    for index, item in enumerate(top_k_dict.items()):
        table_data.append({'id': index+1, 'url': item[1][1], 'title': item[1][2], 'count': item[1][0]})


    return table_data



# 返回 页面访问总时间的URL的数据
def table_data_url_time_rank(history_data):

    # 频率字典
    dict_data = {}

    # 对历史记录文件进行遍历
    for data in history_data:
        url_id = data[0]
        key = url_id

        if (key in dict_data.keys()):
            # 存储url访问时间(小时)，精确到小数点后两位
            dict_data[key][0] += round(data[8]/1000000/3600, 2)
            # 存储url地址
            dict_data[key][1] = data[1]
            # 存储url标题
            dict_data[key][2] = data[2]

        else:
            dict_data[key] = [0.0, '', '']



    # 筛选出前k=10个频率最高的数据
    top_k_dict = get_top_k_from_dict_value_1(dict_data, 100)
    # print(top_k_dict)

    # 返回的table data数据
    table_data = []

    for index, item in enumerate(top_k_dict.items()):
        table_data.append({'id': index+1, 'url': item[1][1], 'title': item[1][2], 'count': item[1][0]})


    return table_data





# 获取历史记录文件中的日期集合
def get_history_date_time(history_data):

    list_date_time = []

    # 对历史记录文件进行遍历
    for data in history_data:
        date_time = data[5]

        # 由于Chrome浏览器在sqlite中存储的时间是以1601-01-01 00:00:00 为起始时间点的微妙计数
        # 与Unix时间戳存在时间间隔，所以需要转换
        unix_time_samp = (date_time / 1000000) - 11644473600

        # 中国以北京时间为准，北京时间为UTC+8小时，8小时=28800秒
        unix_time_samp += 28800

        # 放入list_date_time列表
        list_date_time.append(unix_time_samp)


    # 将时间转化为标准格式
    for i in range(len(list_date_time)):
        unix_time_samp = list_date_time[i]
        list_date_time[i] = time.strftime("%Y-%m-%d", time.gmtime(unix_time_samp))

    # 去重复，set表示集合，集合不可能存在重复元素
    list_unique = list(set(list_date_time))

    # 升序排序
    list_unique_sort = sorted(list_unique)

    # print(list_unique_sort)
    return list_unique_sort





# 绘制 某日不同时刻访问次数 散点图
def plot_scatter_website_diff_time(date_time_value, history_data):

    # 非法输入日期
    if date_time_value is None:
        return {}

    # print(date_time_value)


    # 频率字典
    dict_data = {}
    for i in range(0, 24):
        dict_data[i] = 0

    # 对历史记录文件进行遍历
    for data in history_data:
        date_time = data[5]

        # 由于Chrome浏览器在sqlite中存储的时间是以1601-01-01 00:00:00 为起始时间点的微妙计数
        # 与Unix时间戳存在时间间隔，所以需要转换
        unix_time_samp = (date_time / 1000000) - 11644473600

        # 中国以北京时间为准，北京时间为UTC+8小时，8小时=28800秒
        unix_time_samp += 28800

        # 获取今天日期
        current_day = time.strftime("%Y-%m-%d", time.gmtime(unix_time_samp))

        # 判断是否是今天
        if(date_time_value == current_day):

            key = time.strftime("%H", time.gmtime(unix_time_samp))
            key = int(key)

            if key in dict_data.keys():
                dict_data[key] += 1

    # print(dict_data)

    max_value_dict = max([i for i in dict_data.values()])
    # max_value_dict说明没有任何元素，直接返回空数据
    if max_value_dict == 0:
        return {}


    figure = go.Figure(
        data=[
            go.Scatter(
                x=[i for i in dict_data.keys()],
                y=[i for i in dict_data.values()],
                name='lines+markers',
                mode='lines+markers',
                marker_color='rgba(55, 83, 109, .8)',
                marker=dict(size=[(i/max_value_dict)*30 for i in dict_data.values()]),
                fill='tozeroy'
            )
        ],

        layout=go.Layout(
            showlegend=False,
            margin=go.layout.Margin(l=40, r=0, t=40, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='时刻(24小时制)'),
            yaxis=dict(title='次数')
        )
    )


    return figure