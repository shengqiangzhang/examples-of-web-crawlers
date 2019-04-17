# -*- coding:utf-8 -*-

from pyecharts import Pie
from pyecharts import Map
import subprocess
from wxpy import *
from platform import system
import os
import subprocess
import shutil
from tqdm import tqdm
from pyecharts import Pie
from pyecharts import Map
from requests import get
from requests import post
from json import loads
from platform import system

if(__name__ == '__main__'):

    # 个性签名列表
    data = ['大家好啊','我叫万钢','这是什么情况\/']

    # 转为string
    data = ','.join(data)

    postData = {'data':data, 'type':'exportword', 'arg':'', 'beforeSend':'undefined'}
    response = post('http://life.chacuo.net/convertexportword',data=postData)
    data = response.text.replace('{"status":1,"info":"ok","data":["','').replace('\/','').replace('\\\\','')

    # 解码，windows与其他系统有所不同
    if ('Windows' in system()):
        data = data.encode('unicode_escape').decode('unicode_escape')
    else:
        data = data.encode('utf-8').decode('unicode_escape')


    # 将返回的分词结果json字符串转化为python对象，并做一些处理
    data = data.split("=====================================")[0]
    data = data.split('  ')



    # 对分词结果数据进行去除一些无意义的词操作
    stop_words = [',', '，', '.', '。', '!', '！', ':', '：', '\'', '‘', '’', '“', '”', '的', '了', '已经', '=', '\r', '\n', '\r\n', '\t', '以下关键词', '[', ']', '{', '}']
    tmp = []
    for x in data:
        if(x not in stop_words):
            tmp.append(x)
    data = tmp

    print(tmp)
    # data = data.replace('    ','')


    # 将分词结果转化为list，根据分词结果，可以知道以2个空格为分隔符
    # data = data.split('  ')

    # print(data)

    # 进行词频统计，结果存入字典signature_dict中
    signature_dict = {}
    for word in data:
        if(word in signature_dict.keys()):
            signature_dict[word] += 1
        else:
            signature_dict[word] = 1

