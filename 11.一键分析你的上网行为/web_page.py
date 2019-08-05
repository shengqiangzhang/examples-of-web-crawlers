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

# dash是一款基于python的web轻量级框架，无需js即可轻松运行
# 适合用于比较简单的web页面的快速部署，如数据可视化，图表展示等
# 复杂页面不建议使用dash进行开发
# dash官网: https://dash.plot.ly/

# 配置一个dash服务器
app = dash.Dash(__name__)

# 设置网页标题
app.title = 'Browser History Analysis'

# html元素布局
# 完全嵌入在python代码中
# 仅适合简单web页面的快速搭建，复杂页面不建议使用dash开发
# 如果你对以下布局代码不了解，请勿随意修改代码
app.layout = html.Div([

    html.Button(
        id = 'load_first',
        children = 'button',
        n_clicks = 0
    ),

    html.Div(
        style={'position': 'relative', 'margin': '0 auto', 'width': '100%', 'padding-bottom': '50%', },
        children=[
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id='graph_website_count_rank',
                        style={'position': 'absolute', 'width': '100%', 'height': '100%', 'top': '0', 'left': '0', 'bottom': '0', 'right': '0'},
                        config={'displayModeBar': False},
                    ),
                ],
                type='dot',
                style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%,-50%)'}
            ),
        ],
    ),
])






# 对url进行简化
def url_simplification(url):
    tmp_url = url

    try:
        url = url.split('//')
        url = url[1].split('/', 1)
        url = url[0].replace("www.", "")
        return url

    except IndexError:
        print('特殊的url')
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






# 回调，用于更新web页面数据
# dash框架是前后端不分离的，所以仅仅适用于简单页面部署，复杂页面不推荐使用dash

# 页面访问频率排名
@app.callback(
    dash.dependencies.Output('graph_website_count_rank', 'figure'),
    [
        dash.dependencies.Input('load_first', 'n_clicks')
    ]
)
def update(n_clicks):
    if(n_clicks > 0):
        # 正确获取到历史记录文件
        if(history_data != 'error'):

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


            # 筛选出前20个频率最高的数据
            top_10_dict = get_top_k_from_dict(dict_data, 20)


            figure = go.Figure(
                data=[
                    go.Bar(
                        x = [i for i in top_10_dict.keys()],
                        y = [i for i in top_10_dict.values()],
                        name='bar',
                        marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                        )
                    )
                ],
                layout=go.Layout(
                    title='访问最多的网站',
                    showlegend=False,
                    margin=go.layout.Margin(l=40, r=0, t=40, b=30),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            )

            return figure

        else:
            # 取消更新页面数据
            raise dash.exceptions.PreventUpdate("cancel the callback")

    else:
        # 取消更新页面数据
        raise dash.exceptions.PreventUpdate("cancel the callback")




# 开始运行web服务器
if __name__ == '__main__':

    # 获取历史记录数据
    history_data = get_history_data()
    #
    # for i in history_data:
    #     print(i)

    # 是否是在本地运行(测试)
    app_local = True

    # 127.0.0.1表示本机可浏览
    # 0.0.0.0表示所有用户均可浏览，一般用于部署到服务器
    if(app_local):
        app.run_server(host='127.0.0.1', debug=True, port='8090')
    else:
        app.run_server(host='0.0.0.0', debug=False, port='8090')