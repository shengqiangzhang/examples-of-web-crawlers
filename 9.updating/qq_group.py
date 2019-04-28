# -*- coding:utf-8 -*-

# 引用自定义库
from element_encrypt import hash33_token
from element_encrypt import hash33_bkn
from url_request import get_html
from url_request import post_html


# 引用第三方库
import requests
import time
import json
from platform import system

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



class QQGroup(object):
    """
    QQ群对象，用于获取指定QQ号的群信息及群成员信息，
    同时，该接口可获取指定QQ的所有好友分组，但是获取的好友数据仅包含备注名和QQ号
    """

    def __init__(self):

        self.is_login = False
        self.cookies_merge_dict = ''


        # 访问网页，为了获取参数pt_login_sig
        login_url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=549000912&s_url=http://qun.qq.com/member.html'
        html = get_html(login_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict1 = requests.utils.dict_from_cookiejar(html.cookies)
        pt_login_sig = cookies_back_dict1['pt_login_sig']

        # 访问网页，为了获取参数ptqrtoken
        qrcode_url = 'https://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.39550762134604156'
        html = get_html(qrcode_url, '')
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
        cookies_merge_dict = {}
        cookies_merge_dict.update(cookies_back_dict1)
        cookies_merge_dict.update(cookies_back_dict2)
        print(u'当前cookies:{}'.format(cookies_merge_dict))

        # 实时检测二维码状态
        while (True):
            # 目标网址
            target_url = 'http://ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fqun.qq.com%2Fmember.html&' + 'ptqrtoken=' + str(
                ptqrtoken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1499652067577&js_ver=10224&js_type=1&login_sig=' + str(
                pt_login_sig) + '&pt_uistyle=40&aid=549000912&'

            # 登录，需要带上访问cookies
            html = get_html(target_url, cookies_merge_dict)

            # 返回的响应码为200说明二维码没过期
            if (html.status_code):
                if ('二维码未失效' in html.text):
                    print(u'当前二维码未失效，请你扫描二维码进行登录')
                elif ('二维码认证' in html.text):
                    print(u'扫描成功，正在认证中')
                elif ('登录成功' in html.text):
                    self.is_login = True
                    print(u'登录成功')
                    break
                if ('二维码已经失效' in html.text):
                    print(u'当前二维码已失效，请重启本软件')
                    exit()

            # 延时
            time.sleep(2)

        # 登录成功后，把返回的cookies合并进去
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        cookies_merge_dict.update(cookies_back_dict)
        print(u'当前cookies:{}'.format(cookies_merge_dict))

        # 登录成功后，会返回一个地址，需要对该地址进行访问以便获取新的返回cookies
        data_list = (html.text.replace("')", '')).split("',")
        url = (data_list[2])[1:]
        # print(url, nick_name)
        # 这里需要注意的是，需要禁止重定向，才能正确获得返回的cookies
        html = requests.get(url, cookies=cookies_merge_dict, allow_redirects=False)
        # 把返回的cookies合并进去
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        cookies_merge_dict.update(cookies_back_dict)
        print(u'当前cookies:{}'.format(cookies_merge_dict))
        self.cookies_merge_dict = cookies_merge_dict



    def get_group(self):

        # 获取所有群基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict['skey'])
        submit_data = {'bkn': bkn}
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_group_list', self.cookies_merge_dict, submit_data)
        group_info = json.loads(html.text)
        print(group_info)
        return group_info['join']

    def get_members_in_group(self,group_number):

        # 获取某个群的群成员
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict['skey'])

        # 由于接口限制每次最多获取20个成员的信息，所以我们先获取一遍，得到群成员的数量，再在后面重复获取几次
        submit_data = {'gc': group_number, 'st': '0', 'end': '0', 'sort': '0', 'bkn': bkn, }
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/search_group_members', self.cookies_merge_dict, submit_data)
        group_member = json.loads(html.text)
        group_count = group_member['count']
        # print(group_count)

        now_count = 0
        members_in_group_list = []
        while(now_count <= group_count):
            if(now_count <= group_count - 20):
                submit_data = {'gc': group_number, 'st': str(now_count), 'end': str(now_count + 20), 'sort': '0', 'bkn': bkn, }
                html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/search_group_members', self.cookies_merge_dict, submit_data)
                group_member = json.loads(html.text)
                # print('end_count:{}'.format(now_count+20))
                # print(group_member['mems'])
                #将群成员数据合并到原有的列表中
                members_in_group_list += group_member['mems']
                now_count += 20
            else:
                submit_data = {'gc': group_number, 'st': str(now_count), 'end': str(group_count), 'sort': '0', 'bkn': bkn, }
                html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/search_group_members', self.cookies_merge_dict, submit_data)
                group_member = json.loads(html.text)
                # print('end_count:{}'.format(group_count))
                # print(group_member['mems'])
                #将群成员数据合并到原有的列表中
                members_in_group_list += group_member['mems']
                now_count += 20


            print(members_in_group_list)
            time.sleep(2)


        # 对得到的群成员列表进行去重操作
        tmp_list = []
        for member in members_in_group_list:
            if member not in tmp_list:
                tmp_list.append(member)

        members_in_group_list = tmp_list
        return members_in_group_list


    def get_all_friends_in_qq(self):

        # 获取所有qq好友基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict['skey'])
        submit_data = {'bkn': bkn}
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_friend_list', self.cookies_merge_dict, submit_data)
        friend_info = json.loads(html.text)
        # print(friend_info['result'])
        return friend_info['result']

    def get_info_in_qq_friend(self,qq_number):

        # 获取某个qq好友的详细信息

        # 需要提交的数据
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict['skey'])
        submit_data = {'keyword':str(qq_number), 'ldw': str(bkn), 'num':'20', 'page':'0', 'sessionid':'0', 'agerg':'0', 'sex':'0', 'firston':'0', 'video':'0', 'country':'1', 'province':'65535', 'city':'0', 'district':'0', 'hcountry':'1', 'hprovince':'0', 'hcity':'0', 'hdistrict':'0', 'online':'0'}

        # 需要提交的cookies
        # cookies = {'uin':self.cookies_merge_dict['uin'], 'skey':self.cookies_merge_dict['skey'], 'ptisp':self.cookies_merge_dict['ptisp'], 'RK':self.cookies_merge_dict['RK'], 'ptcz':self.cookies_merge_dict['ptcz']}

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://find.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://find.qq.com/'
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,post方式
        html = requests.post('http://cgi.find.qq.com/qqfind/buddy/search_v3', data=submit_data, cookies=self.cookies_merge_dict, headers=header, verify=False)

        # 将好友信息解析为python对象
        friend_info = json.loads(html.text)
        print(friend_info)
        return friend_info['result']['buddy']['info_list'][0]



    def get_profile_picture(self, qq_number, size=100):
        # 获取指定qq的头像，size的值可为40、100、140，默认为100
        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,get方式
        # https://q4.qlogo.cn/g?b=qq&nk=10000&s=140
        html = requests.get('https://q4.qlogo.cn/g?b=qq&nk=' + str(qq_number) + '&s=' + str(size), verify=False)
        return html.content

