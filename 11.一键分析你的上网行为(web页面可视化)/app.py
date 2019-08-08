#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app.py
@author: Shengqiang Zhang
@time: 2019/8/6 02:53
@mail: sqzhang77@gmail.com
"""

from browser_history_analysis import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol

import time


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


    # fork me on github 挂件
    html.Div(
        children=[
            html.A(
                href='https://github.com/shengqiangzhang/examples-of-web-crawlers/tree/master/11.%E4%B8%80%E9%94%AE%E5%88%86%E6%9E%90%E4%BD%A0%E7%9A%84%E4%B8%8A%E7%BD%91%E8%A1%8C%E4%B8%BA(web%E9%A1%B5%E9%9D%A2%E5%8F%AF%E8%A7%86%E5%8C%96)',
                target='_blank',
                children=[
                    html.Img(
                        src='https://camo.githubusercontent.com/652c5b9acfaddf3a9c326fa6bde407b87f7be0f4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6f72616e67655f6666373630302e706e67',
                        alt='Fork me on GitHub',
                        style={'position': 'absolute', 'top': 0, 'right': 0, 'border': 0}
                    )
                ]
            )
        ]
    ),


    # 页面访问次数排名
    html.Div(
        style={'margin-bottom':'150px'},
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
                        value=10,
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


    # 页面访问停留时间排名
    html.Div(
        style={'margin-bottom': '150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='页面访问停留时间排名',
                        style={'font-weight': 'bold', 'color': 'red'}
                    )
                ]
            ),

            html.Div(
                style={"overflowY": "scroll"},
                children=[
                    dash_table.DataTable(
                        id='table_url_time_rank',
                        columns=[
                            {'name': '编号', 'id': 'id'},
                            {'name': '停留时间', 'id': 'count', 'type': 'numeric', 'format': Format(nully='N/A', precision=2, scheme=Scheme.decimal, sign=Sign.parantheses, symbol=Symbol.yes, symbol_suffix=u'小时')},
                            {'name': '网页地址', 'id': 'url'},
                            {'name': '网页标题', 'id': 'title'}

                        ],
                        data=[
                            {'id': '0', 'url': '初始化', 'title': '初始化', 'count': '初始化'}
                        ],
                        style_header={
                            'fontWeight': 'bold',
                            'backgroundColor': 'white',
                            'borderBottom': '1px solid black',
                        },
                        style_cell={
                            'textAlign': 'left',
                            'fontSize': '15px',
                            'border': '1px solid grey'
                        },
                        style_table={
                            'minHeight': '1px',
                            'maxHeight': '400px',
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ]

                    )
                ],
            )
        ]
    ),





    # 每日页面访问次数散点图
    html.Div(
        style={'margin-bottom':'150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='每日页面访问次数',
                        style={'font-weight': 'bold', 'color': 'red'}
                    )
                ]
            ),

            html.Div(
                style={'position': 'relative', 'margin': '0 auto', 'width': '100%', 'padding-bottom': '50%', },
                children=[
                    dcc.Loading(
                        children=[
                            dcc.Graph(
                                id='graph_day_count_rank',
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

    # 访问次数最多的10个URL
    html.Div(
        style={'margin-bottom': '150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='访问次数最多的100个URL',
                        style={'font-weight': 'bold', 'color': 'red'}
                    )
                ]
            ),

            html.Div(
                style={"overflowY": "scroll"},
                children=[
                    dash_table.DataTable(
                        id='table_url_count_rank',
                        columns=[
                            {'name': '编号', 'id': 'id'},
                            {'name': '访问次数', 'id': 'count'},
                            {'name': '网页地址', 'id': 'url'},
                            {'name': '网页标题', 'id': 'title'}
                        ],
                        data=[
                            {'id': '0', 'url': '初始化', 'title': '初始化', 'count': '初始化'}
                        ],
                        style_header={
                            'fontWeight': 'bold',
                            'backgroundColor': 'white',
                            'borderBottom': '1px solid black',
                        },
                        style_cell={
                            'textAlign': 'left',
                            'fontSize': '15px',
                            'border': '1px solid grey'
                        },
                        style_table={
                            'minHeight': '1px',
                            'maxHeight': '400px',
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ]

                    )
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




# 绘制 每日访问次数 散点图
def plot_scatter_website_count_rank():
    global history_data

    # 频率字典
    dict_data = {}

    # 对历史记录文件进行遍历
    for data in history_data:
        date_time = data[5]

        # 由于Chrome浏览器在sqlite中存储的时间是以1601-01-01 00:00:00 为起始时间点的微妙计数
        # 与Unix时间戳存在时间间隔，所以需要转换
        unix_time_samp = (date_time / 1000000) - 11644473600
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
                marker=dict(size=[(i/max_value_dict)*30 for i in dict_sort_data.values()])
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
def table_data_url_count_rank():
    global history_data

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
def table_data_url_time_rank():
    global history_data

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
    print(top_k_dict)

    # 返回的table data数据
    table_data = []

    for index, item in enumerate(top_k_dict.items()):
        table_data.append({'id': index+1, 'url': item[1][1], 'title': item[1][2], 'count': item[1][0]})


    return table_data




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





# 每日访问次数
@app.callback(
    dash.dependencies.Output('graph_day_count_rank', 'figure'),
    [
        dash.dependencies.Input('auto_find_text_flag', 'value')
    ]
)
def update(auto_find_text_flag):

    global history_data
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

    global history_data
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

    global history_data
    # 正确获取到历史记录文件
    if (history_data != 'error' and auto_find_text_flag == 1):
        table_data = table_data_url_time_rank()
        return table_data
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



    # 初始化历史记录文件，默认为error状态，即未找到状态
    # 在web页面刷新时，自动触发回调，更新history_data的值
    history_data = 'error'

    # 是否是在本地运行(测试)
    app_local = False


    # 127.0.0.1表示本机可浏览
    # 0.0.0.0表示所有用户均可浏览，一般用于部署到服务器
    if(app_local):
        app.run_server(host='127.0.0.1', debug=False, port='8090')
    else:
        app.run_server(host='0.0.0.0', debug=False, port='8090')