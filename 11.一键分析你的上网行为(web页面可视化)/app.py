#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app.py
@author: Shengqiang Zhang
@time: 2019/8/6 02:53
@mail: sqzhang77@gmail.com
"""


from app_configuration import app
from app_layout import app_layout
from app_callback import app_callback_function



# 设置网页标题
app.title = 'Browser History Analysis'

# 开启加载本地css和js文件模式
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# html元素布局
# 完全嵌入在python代码中
# 仅适合简单web页面的快速搭建，复杂页面不建议使用dash开发
# 如果你对以下布局代码不了解，请勿随意修改代码
app.layout = app_layout



# 回调，用于更新web页面数据
# dash框架是前后端不分离的，所以仅仅适用于简单页面部署，复杂页面不推荐使用dash
app_callback_function()



# 开始运行web服务器
if __name__ == '__main__':


    # 是否是在本地运行(测试)
    app_local = False

    # 127.0.0.1表示本机可浏览
    # 0.0.0.0表示所有用户均可浏览，一般用于部署到服务器
    # 若部署到服务器，请务必在云控制面板的防火墙中允许8090端口
    if(app_local):
        app.run_server(host='127.0.0.1', debug=True, port='8090')
    else:
        app.run_server(host='0.0.0.0', debug=False, port='8090')