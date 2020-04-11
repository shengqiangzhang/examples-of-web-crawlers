#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: test.py
@author: Shengqiang Zhang
@time: 2020/4/11 14:48
@mail: sqzhang77@gmail.com
"""

import sys
from PyQt5.QtCore import QUrl,pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile,QWebEngineSettings,QWebEnginePage
class sample(QWebEngineView):
    DomainCookies = {}
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('cookie操作演示')
        url = 'https://weread.qq.com/#login'
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.loadFinished.connect(self.onLoadFinished)
        self.show()
        self.load(QUrl(url))

    def onLoadFinished(self):
        for name in self.DomainCookies:
            print(name,self.DomainCookies[name])

    def onCookieAdd(self, cookie):
        if 'weread.qq.com' in cookie.domain():
            name = cookie.name().data().decode('utf-8')
            value = cookie.value().data().decode('utf-8')
            if name not in self.DomainCookies:
                self.DomainCookies.update({name: value})
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = sample()
    sys.exit(app.exec_())