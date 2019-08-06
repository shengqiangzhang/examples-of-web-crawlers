#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: web_page.py
@author: Shengqiang Zhang
@time: 2019/8/6 02:53
@mail: sqzhang77@gmail.com
"""

from browser_history_analysis import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import time
from datetime import datetime

# dash是一款基于python的web轻量级框架，无需js即可轻松运行
# 适合用于比较简单的web页面的快速部署，如数据可视化，图表展示等
# 复杂页面不建议使用dash进行开发
# dash官网: https://dash.plot.ly/

# 配置一个dash服务器
app = dash.Dash(__name__)

# 设置网页标题
app.title = 'Browser History Analysis'

# 加载本地css和js文件
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# html元素布局
# 完全嵌入在python代码中
# 仅适合简单web页面的快速搭建，复杂页面不建议使用dash开发
# 如果你对以下布局代码不了解，请勿随意修改代码
app.layout = html.Div([

    html.Div(
        className = 'row',
        children=[
            dcc.Input(
                id='first_load_web_page',
                type = 'number',
                value=0,
                style={'display': 'none'}
            ),

            dcc.Input(
                id = 'auto_find_text_flag',
                type = 'number',
                value = 0,
                style = {'display':'none'}
            ),
        ]
    ),


    html.Div(
        children=[
            html.Div(
                style={'border-top-style':'solid', 'border-bottom-style':'solid'},
                className='row',
                children=[
                    html.Span(
                        children='页面访问次数排名, ',
                        style={'font-weight': 'bold', 'color':'red'}
                    ),

                    html.Span(
                        children='显示个数:',
                    ),
                    dcc.Input(
                        id='input_website_count_rank',
                        type='text',
                        value=20,
                        style={'margin-top':'10px', 'margin-bottom':'10px'}
                    ),
                ]
            ),

            html.Div(
                style={'position': 'relative', 'margin': '0 auto', 'width': '100%', 'padding-bottom': '50%', },
                children=[
                    dcc.Loading(
                        children=[
                            dcc.Graph(
                                id='graph_website_count_rank',
                                style={'position': 'absolute', 'width': '100%', 'height': '100%', 'top': '0',
                                       'left': '0', 'bottom': '0', 'right': '0'},
                                config={'displayModeBar': False},
                            ),
                        ],
                        type='dot',
                        style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%,-50%)'}
                    ),
                ],
            )
        ]
    ),


])






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


# 获取字典的前k个最大的子集合
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
def plot_bar_website_count_rank(value):

    global history_data

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












# 回调，用于更新web页面数据
# dash框架是前后端不分离的，所以仅仅适用于简单页面部署，复杂页面不推荐使用dash

# 页面访问频率排名
@app.callback(
    dash.dependencies.Output('graph_website_count_rank', 'figure'),
    [
        dash.dependencies.Input('input_website_count_rank', 'value'),
        dash.dependencies.Input('auto_find_text_flag', 'value')
    ]
)
def update(value, auto_find_text_flag):

    global history_data
    # 正确获取到历史记录文件
    if (history_data != 'error' and auto_find_text_flag == 1):
        figure = plot_bar_website_count_rank(value)
        return figure
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
    if(value is not None):
        # 获取历史记录数据
        global history_data
        history_data = get_history_data()
        for i in history_data:
            print(i)

        if(history_data != 'error'):
            # 找到
            return 1
        else:
            # 没找到
            return 0
    else:
        return 0


# 开始运行web服务器
if __name__ == '__main__':

    time_c = 13209575098047540 / 1000000 - 11644473600
    print(time_c)
    print(time.strftime("%Y-%m-%d %X", time.gmtime(time_c)))

    # 初始化历史记录文件，默认为error状态，即未找到状态
    # 在web页面刷新时，自动触发回调，更新history_data的值
    history_data = 'error'

    # 是否是在本地运行(测试)
    app_local = True


    # 127.0.0.1表示本机可浏览
    # 0.0.0.0表示所有用户均可浏览，一般用于部署到服务器
    if(app_local):
        app.run_server(host='127.0.0.1', debug=False, port='8090')
    else:
        app.run_server(host='0.0.0.0', debug=False, port='8090')