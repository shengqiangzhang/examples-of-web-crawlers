# -*- coding:utf-8 -*-

from tkinter import Tk
from tkinter import Label
from tkinter import Frame
from tkinter import Text
from tkinter import Scrollbar
from tkinter.constants import *

# 创建一个根窗口，其余的控件都要在这个窗口上面
root = Tk()
# 创建一个图像框
image_label = Label(root)
# 创建一个容器
frame = Frame(root)
# 在这个容器上创建文本框text
text = Text(frame, height=9)
# 在这个容器上创建滚动条
scroll = Scrollbar(frame)


# 自定义输出数据
# 定义可变参数
def custom_print(*args):
    for data in args:

        # 将data转化为string类型
        data = str(data)

        # 正常调试输出
        print(data)
        # 将内容输出到文本框
        text.insert(END, data + '\n')
        # 设置文本框当前显示的内容为最底部的内容
        text.see(END)


class gui(object):

    """
    tkinter对象，用于绘制基本的gui界面
    """
    def __init__(self):
        self.root = root
        self.image_label = image_label
        self.frame = frame
        self.text = text
        self.scroll = scroll

        # 设置禁止调整窗口大小
        root.resizable(False, False)
        # 设置窗口标题
        root.title('一键生成qq个人历史报告')
        # 设置窗口大小及其位置
        self.center_window(800, 160)

        # 设置图像框
        image_label.pack(side=LEFT, anchor=NE)

        # 设置容器
        frame.pack(side=RIGHT, anchor=NW)
        # 将滚动条填充
        # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        scroll.pack(side=RIGHT, fill=Y)
        # 将文本框填充进root窗口的左侧
        text.pack(side=LEFT)
        # 将滚动条与文本框关联
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        # 设置文本框内容
        text.insert(END, '加载中...\n')

        # 让根窗口进入事件循环
        self.root.mainloop()


    # 设置主窗口大小及其位置
    def center_window(self, w, h):
        # 获取屏幕 宽、高
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))