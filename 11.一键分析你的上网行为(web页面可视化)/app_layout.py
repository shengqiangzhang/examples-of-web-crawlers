#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app_layout.py
@author: Shengqiang Zhang
@time: 2019/8/10 01:09
@mail: sqzhang77@gmail.com
"""

import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_table.Format import Format, Scheme, Sign, Symbol



# html元素布局
# 完全嵌入在python代码中
# 仅适合简单web页面的快速搭建，复杂页面不建议使用dash开发
# 如果你对以下布局代码不了解，请勿随意修改代码
app_layout = html.Div([

    html.Div(
        className = 'row',
        children=[

            dcc.Input(
                id='upload_file_success_flag',
                type='number',
                value=1,
                style={'display': 'none'}
            ),

            # 在浏览器中存储数据，每次刷新页面或者载入页面都会被清空
            dcc.Store(id='store_memory_history_data')
        ]
    ),


    # 上传历史记录文件
    html.Div(
        className='row',
        children=[
            html.Div(
                className='five columns',
                children=[
                    dcc.Upload(
                        id='dcc_upload_file',
                        children=html.Div([
                            html.A(
                                id='upload_link',
                                children='点击上传Chrome历史记录文件',
                                style={'cursor': 'pointer'}
                            )
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin-top': '10px',
                            'margin-bottom': '20px'
                        },

                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                ]
            ),


            html.Div(
                className='five columns',
                children=[
                    html.Div(
                        style={'margin-top':'10px'},
                        className='row',
                        children=[
                            html.A(
                                children='问题1: 如何获取Chrome历史记录文件?',
                                href='assets/static/help.html',
                                target='_blank',
                                style={'cursor': 'pointer', 'color':'red'}
                            ),
                        ]
                    ),

                    html.Div(
                        style={'margin-top':'10px'},
                        className='row',
                        children=[
                            html.A(
                                children='问题2: 是否存在窃取隐私问题?',
                                href='assets/static/help.html#privacy',
                                target='_blank',
                                style={'cursor': 'pointer', 'color':'red'}
                            ),
                        ]
                    ),
                ]
            )
        ]
    ),



    # fork me on github 挂件
    html.Div(
        # 设置这个div位于最顶层，防止被其他DIV覆盖
        children=[
            html.A(
                href='https://github.com/shengqiangzhang/examples-of-web-crawlers/tree/master/11.%E4%B8%80%E9%94%AE%E5%88%86%E6%9E%90%E4%BD%A0%E7%9A%84%E4%B8%8A%E7%BD%91%E8%A1%8C%E4%B8%BA(web%E9%A1%B5%E9%9D%A2%E5%8F%AF%E8%A7%86%E5%8C%96)',
                target='_blank',
                children=[
                    html.Img(
                        src='https://camo.githubusercontent.com/652c5b9acfaddf3a9c326fa6bde407b87f7be0f4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6f72616e67655f6666373630302e706e67',
                        alt='Fork me on GitHub',
                        style={'position': 'absolute', 'top': 0, 'right': 0, 'border': 0, 'z-index': '99999'}
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


    # 页面访问停留总时间排名
    html.Div(
        style={'margin-bottom': '150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='页面访问停留总时间排名',
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



    # 某日不同时刻访问次数散点图
    html.Div(
        style={'margin-bottom': '150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='某日不同时刻访问次数, 选择时刻: ',
                        style={'font-weight': 'bold', 'color': 'red', 'line-height':'34px', 'margin-right': '10px', 'float':'left'}
                    ),

                    dcc.Dropdown(
                        id = 'dropdown_time_1',
                        className='three columns',
                        options=[
                            {'label': '初始化', 'value': '初始化'}
                        ],
                        clearable=False,
                        searchable=False
                    )
                ]
            ),

            html.Div(
                style={'position': 'relative', 'margin': '0 auto', 'width': '100%', 'padding-bottom': '50%', },
                children=[
                    dcc.Loading(
                        children=[
                            dcc.Graph(
                                id='graph_day_diff_time_count',
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


    # 搜索关键词排名
    html.Div(
        style={'margin-bottom': '150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='搜索关键词排名',
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
                                id='graph_search_word_count_rank',
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



    # 搜索引擎使用情况
    html.Div(
        # style={'margin-bottom': '150px'},
        children=[
            html.Div(
                style={'border-top-style': 'solid', 'border-bottom-style': 'solid'},
                className='row',
                children=[
                    html.Span(
                        children='搜索引擎使用情况',
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
                                id='graph_search_engine_count_rank',
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

    # 底部
    html.Div(
        style={'text-align':'center'},
        children=[
            html.A(
                children=[
                    html.Img(
                        src="assets/image/GitHub-Mark-Light.png",
                        style={'margin': '0 auto', 'width':'50px'}
                    )
                ],
                href='https://github.com/shengqiangzhang/examples-of-web-crawlers/tree/master/11.%E4%B8%80%E9%94%AE%E5%88%86%E6%9E%90%E4%BD%A0%E7%9A%84%E4%B8%8A%E7%BD%91%E8%A1%8C%E4%B8%BA(web%E9%A1%B5%E9%9D%A2%E5%8F%AF%E8%A7%86%E5%8C%96)',
                target='_blank'
            ),

        ]
    )

])
