# -*- coding:utf-8 -*-

import requests
from platform import system
import time
import json

# 引入打开文件所用的库
# Window与Linux和Mac OSX有所不同
# lambda用来定义一个匿名函数，可实现类似c语言的define定义
if('Windows' in system()):
    # Windows
    from os import startfile
    open_file_by_system = lambda x : startfile(x)
elif('Darwin' in system()):
    # MacOSX
    from subprocess import call
    open_file_by_system = lambda x : call(["open", x])
else:
    # Linux
    from subprocess import call
    open_file_by_system = lambda x: call(["xdg-open", x])



# get访问网页
def get_html(url,submit_cookies):

    # 设置请求头,模拟人工
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer' : 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=549000912&s_url=http://qun.qq.com/member.html'
    }
    # 屏蔽https证书警告
    requests.packages.urllib3.disable_warnings()

    # 网页访问,get方式
    html = requests.get(url, cookies = submit_cookies, headers=header, verify=False)

    return html


# post访问网页
def post_html(url,submit_cookies,submit_data):

    # 设置请求头,模拟人工
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer' : 'https://qun.qq.com/member.html'
    }
    # 屏蔽https证书警告
    requests.packages.urllib3.disable_warnings()

    # 网页访问,post方式
    html = requests.post(url, data=submit_data, cookies = submit_cookies, headers=header, verify=False)

    return html


# 对qrsig进行基本的加密，该加密函数由抓包获得，需要具备一定抓包知识才能找到该加密函数
# 根据javascript版的加密函数，将其改写成python版本
def hash33_token(t):
    e, n = 0, len(t)

    for i in range(0,n):
        e += (e << 5) + ord(t[i])

    return 2147483647 & e

# 对skey进行基本的加密，该加密函数由抓包获得，需要具备一定抓包知识才能找到该加密函数
# 根据javascript版的加密函数，将其改写成python版本
def hash33_bkn(skey):
    e = skey
    t = 5381

    for n in range(0,len(e)):
        t += (t << 5) + ord(e[n])

    return 2147483647 & t



if __name__ == "__main__":


    # 访问网页，为了获取参数pt_login_sig
    login_url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=549000912&s_url=http://qun.qq.com/member.html'
    html = get_html(login_url,'')
    # 对返回的cookies进行转化为dict类型，方便处理
    cookies_back_dict1 = requests.utils.dict_from_cookiejar(html.cookies)
    pt_login_sig = cookies_back_dict1['pt_login_sig']

    # 访问网页，为了获取参数ptqrtoken
    qrcode_url = 'https://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.39550762134604156'
    html = get_html(qrcode_url,'')
    # 对返回的cookies进行转化为dict类型，方便处理
    cookies_back_dict2 = requests.utils.dict_from_cookiejar(html.cookies)
    qrsig = cookies_back_dict2['qrsig']
    ptqrtoken = hash33_token(qrsig)

    # 将登录二维码写到本地，并自动打开，让用户扫描
    with open('qrcode.png', "wb") as f:
        f.write(html.content)

    # 调用系统默认打开方式，打开该二维码
    open_file_by_system('qrcode.png')


    # 对返回的两个cookies进行合并，作为提交cookies
    cookies_merge_dict1 = {}
    cookies_merge_dict1.update(cookies_back_dict1)
    cookies_merge_dict1.update(cookies_back_dict2)
    print(u'当前cookies:{}'.format(cookies_merge_dict1))

    # 实时检测二维码状态
    while (True):
        # 目标网址
        target_url = 'http://ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fqun.qq.com%2Fmember.html&' + 'ptqrtoken=' + str(ptqrtoken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1499652067577&js_ver=10224&js_type=1&login_sig=' + str(pt_login_sig) + '&pt_uistyle=40&aid=549000912&'

        # 登录，需要带上访问cookies
        html = get_html(target_url,cookies_merge_dict1)

        # 返回的响应码为200说明二维码没过期
        if(html.status_code):
            if('二维码未失效' in html.text):
                print(u'当前二维码未失效，请你扫描二维码进行登录')
            elif('二维码认证' in html.text):
                print(u'扫描成功，正在认证中')
            elif('登录成功' in html.text):
                print(u'登录成功')
                break
            if ('二维码已经失效' in html.text):
                print(u'当前二维码已失效，请重启本软件')
                exit()

        # 延时
        time.sleep(2)


    # 登录成功后，把返回的cookies合并进去
    cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
    cookies_merge_dict1.update(cookies_back_dict)
    print(u'当前cookies:{}'.format(cookies_merge_dict1))

    # 登录成功后，会返回一个地址，需要对该地址进行访问以便获取新的返回cookies
    data_list = (html.text.replace("')",'')).split("',")
    url = (data_list[2])[1:]
    nick_name = ((data_list[len(data_list)-1])[1:])
    # print(url, nick_name)
    # 这里需要注意的是，需要禁止重定向，才能正确获得返回的cookies
    html = requests.get(url, cookies=cookies_merge_dict1, allow_redirects=False)
    # 把返回的cookies合并进去
    cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
    cookies_merge_dict1.update(cookies_back_dict)
    print(u'当前cookies:{}'.format(cookies_merge_dict1))


    # 获取群信息
    # bkn由参数skey通过另一个加密函数得到
    bkn = hash33_bkn(cookies_merge_dict1['skey'])
    submit_data = {'bkn': bkn}
    html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_group_list', cookies_merge_dict1, submit_data)
    group_info = json.loads(html.text)
    print(group_info['join'])
    for i in group_info['join']:
        print(i)

    # 获取qq好友信息
    # bkn由参数skey通过另一个加密函数得到
    bkn = hash33_bkn(cookies_merge_dict1['skey'])
    submit_data = {'bkn': bkn}
    html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_friend_list', cookies_merge_dict1, submit_data)
    friend_info = json.loads(html.text)
    # print(friend_info['result'])
    for friend_group in friend_info['result'].keys():
        print(friend_info['result'][friend_group])
        print('\n')


    # 获取某个群的群成员
    # bkn由参数skey通过另一个加密函数得到
    bkn = hash33_bkn(cookies_merge_dict1['skey'])
    submit_data = {'gc':'958751361', 'st':'0', 'end':'20', 'sort':'0', 'bkn': bkn, }
    html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/search_group_members', cookies_merge_dict1, submit_data)
    group_member = json.loads(html.text)
    print(group_member)
    print(group_member['count'])


