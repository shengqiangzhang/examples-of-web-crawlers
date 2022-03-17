# -*- coding:utf-8 -*-

# 引用第三方库
# import requests
from requests.packages import urllib3
from requests import get
from requests import post


# get访问网页
def get_html(url,submit_cookies):

    # 设置请求头,模拟人工
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Referer': 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=549000912&s_url=http://qun.qq.com/member.html'
    }
    # 屏蔽https证书警告
    urllib3.disable_warnings()

    # 网页访问,get方式
    html = get(url, cookies=submit_cookies, headers=header, verify=False)

    return html


# post访问网页
def post_html(url,submit_cookies,submit_data):

    # 设置请求头,模拟人工
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Referer' : 'https://qun.qq.com/member.html'
    }
    # 屏蔽https证书警告
    urllib3.disable_warnings()

    # 网页访问,post方式
    html = post(url, data=submit_data, cookies=submit_cookies, headers=header, verify=False)

    return html