import requests
import random
import re
import queue
import threading
import csv
import json
from bs4 import BeautifulSoup


class FundDataScrapy:
    def __init__(self, user_agent_list=[], referer_list=[]):
        self.user_agent_list = user_agent_list
        self.referer_list = referer_list
        self.proxy = self.proxy_pool()
        self.fund_code_list = self.get_fund_code()
        self.fund_length = len(self.fund_code_list)
        self.fund_code_queue = queue.Queue(self.fund_length)
        self.que_put()
        self.mutex_lock = threading.Lock()

    def que_put(self):
        for i in range(self.fund_length):
            self.fund_code_queue.put(self.fund_code_list[i][0])

    def get_fund_code(self):
        header = {'User-Agent': random.choice(self.user_agent_list),
                  'Referer': random.choice(self.referer_list)
                  }
        req = requests.get('http://fund.eastmoney.com/js/fundcode_search.js', timeout=5, headers=header)
        fund_code = req.content.decode()
        fund_code = fund_code.replace("﻿var r = [", "").replace("];", "")
        fund_code = re.findall(r"[\[](.*?)[\]]", fund_code)
        fund_code_list = []
        for sub_data in fund_code:
            data = sub_data.replace("\"", "").replace("'", "")
            data_list = data.split(",")
            fund_code_list.append(data_list)

        return fund_code_list

    def proxy_pool(self):
        url = "https://proxygather.com/zh"
        resp = requests.get(url)
        proxy_list = []
        if resp.status_code == 200:
            demo = resp.content
            soup = BeautifulSoup(demo, 'lxml')
            src = soup.select('script')[7:-4]
            for i in src:
                temp = json.loads(
                    str(i).replace('<script type="text/javascript">', '').replace('</script>', '').replace(
                        'gp.insertPrx(',
                        '').replace(');',
                                    ''))
                proxy_list.append({'http': temp['PROXY_IP'] + ':' + str(int(temp['PROXY_PORT'], 16))})
        return proxy_list

    def get_fund_data(self):
        while (not self.fund_code_queue.empty()):
            fund_code = self.fund_code_queue.get()
            header = {'User-Agent': random.choice(user_agent_list),
                      'Referer': random.choice(referer_list)
                      }
            emp.append(fund_code)
            try:
                req = requests.get("http://fundgz.1234567.com.cn/js/" + str(fund_code) + ".js",
                                   proxies=random.choice(self.proxy),
                                   timeout=3, headers=header)
                data = (req.content.decode()).replace("jsonpgz(", "").replace(");", "").replace("'", "\"")
                data_dict = json.loads(data)
                self.mutex_lock.acquire()
                with open('./fund_data.csv', 'a+', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    data_list = [x for x in data_dict.values()]
                    csv_writer.writerow(data_list)
                self.mutex_lock.release()
            except Exception:
                self.fund_code_queue.put(fund_code)

    def start_scrapy(self):
        for i in range(100):
            t = threading.Thread(target=self.get_fund_data, name='ThreadName' + str(i))
            t.start()


if __name__ == '__main__':
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
    ]

    referer_list = [
        'http://fund.eastmoney.com/110022.html',
        'http://fund.eastmoney.com/110023.html',
        'http://fund.eastmoney.com/110024.html',
        'http://fund.eastmoney.com/110025.html'
    ]
    fds = FundDataScrapy(user_agent_list, referer_list)
    fds.start_scrapy()
