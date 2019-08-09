#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app_configuration.py
@author: Shengqiang Zhang
@time: 2019/8/10 01:23
@mail: sqzhang77@gmail.com
"""

import dash


# dash是一款基于python的web轻量级框架，无需js即可轻松运行
# 适合用于比较简单的web页面的快速部署，如数据可视化，图表展示等
# 复杂页面不建议使用dash进行开发
# dash官网: https://dash.plot.ly/

# 配置一个dash服务器
app = dash.Dash(__name__)