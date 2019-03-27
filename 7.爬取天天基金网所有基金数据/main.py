# -*- coding:utf-8 -*-

import requests
import random
import re
import queue
import threading
import csv
import json

# user_agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

# referer列表
referer_list = [
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/110024.html',
    'http://fund.eastmoney.com/110025.html'
]



# 返回一个可用代理，格式为ip:端口
# 该接口直接调用github代理池项目给的例子，故不保证该接口实时可用
# 建议自己搭建一个本地代理池，这样获取代理的速度更快
# 代理池搭建github地址https://github.com/1again/ProxyPool
# 搭建完毕后，把下方的proxy.1again.cc改成你的your_server_ip，本地搭建的话可以写成127.0.0.1或者localhost
def get_proxy():
    data_json = requests.get("http://proxy.1again.cc:35050/api/v1/proxy/?type=2").text
    data = json.loads(data_json)
    return data['data']['proxy']


# 获取所有基金代码
def get_fund_code():
    # 获取一个随机user_agent和Referer
    header = {'User-Agent': random.choice(user_agent_list),
              'Referer': random.choice(referer_list)
    }

    # 访问网页接口
    req = requests.get('http://fund.eastmoney.com/js/fundcode_search.js', timeout=5, headers=header)

    # 获取所有基金代码
    fund_code = req.content.decode()
    fund_code = fund_code.replace("﻿var r = [","").replace("];","")

    # 正则批量提取
    fund_code = re.findall(r"[\[](.*?)[\]]", fund_code)

    # 对每行数据进行处理，并存储到fund_code_list列表中
    fund_code_list = []
    for sub_data in fund_code:
        data = sub_data.replace("\"","").replace("'","")
        data_list = data.split(",")
        fund_code_list.append(data_list)

    return fund_code_list


# 获取基金数据
def get_fund_data():

    # 当队列不为空时
    while (not fund_code_queue.empty()):

        # 从队列读取一个基金代码
        # 读取是阻塞操作
        fund_code = fund_code_queue.get()

        # 获取一个代理，格式为ip:端口
        proxy = get_proxy()

        # 获取一个随机user_agent和Referer
        header = {'User-Agent': random.choice(user_agent_list),
                  'Referer': random.choice(referer_list)
        }

        # 使用try、except来捕获异常
        # 如果不捕获异常，程序可能崩溃
        try:
            # 使用代理访问
            req = requests.get("http://fundgz.1234567.com.cn/js/" + str(fund_code) + ".js", proxies={"http": proxy}, timeout=3, headers=header)

            # 没有报异常，说明访问成功
            # 获得返回数据
            data = (req.content.decode()).replace("jsonpgz(","").replace(");","").replace("'","\"")
            data_dict = json.loads(data)
            print(data_dict)

            # 申请获取锁，此过程为阻塞等待状态，直到获取锁完毕
            mutex_lock.acquire()

            # 追加数据写入csv文件，若文件不存在则自动创建
            with open('./fund_data.csv', 'a+', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                data_list = [x for x in data_dict.values()]
                csv_writer.writerow(data_list)

            # 释放锁
            mutex_lock.release()

        except Exception:
            # 访问失败了，所以要把我们刚才取出的数据再放回去队列中
            fund_code_queue.put(fund_code)
            print("访问失败，尝试使用其他代理访问")


if __name__ == '__main__':

    # 获取所有基金代码
    fund_code_list = get_fund_code()

    # 将所有基金代码放入先进先出FIFO队列中
    # 队列的写入和读取都是阻塞的，故在多线程情况下不会乱
    # 在不使用框架的前提下，引入多线程，提高爬取效率
    # 创建一个队列
    fund_code_queue = queue.Queue(len(fund_code_list))
    # 写入基金代码数据到队列
    for i in range(len(fund_code_list)):
        #fund_code_list[i]也是list类型，其中该list中的第0个元素存放基金代码
        fund_code_queue.put(fund_code_list[i][0])



    # 创建一个线程锁，防止多线程写入文件时发生错乱
    mutex_lock = threading.Lock()
    # 线程数为50，在一定范围内，线程数越多，速度越快
    for i in range(50):
        t = threading.Thread(target=get_fund_data,name='LoopThread'+str(i))
        t.start()
