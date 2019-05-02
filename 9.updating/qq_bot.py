# -*- coding:utf-8 -*-

# 引用自定义库
from element_encrypt import hash33_token
from element_encrypt import hash33_bkn
from element_encrypt import get_sck
from url_request import get_html
from url_request import post_html


# 引用第三方库
import requests
import time
import json
import re
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



class Bot(object):
    """
    QQ机器人对象，用于获取指定QQ号的群信息及群成员信息，
    同时，该接口可获取指定QQ的所有好友分组，但是获取的好友数据仅包含备注名和QQ号
    """

    def __init__(self):
        self.is_login = False
        self.cookies_merge_dict_in_id_qq_com = {}
        self.cookies_merge_dict_in_qun_qq_com = {}
        self.qq_number = ''
        self.login_id_qq_com()
        self.login_qun_qq_com()

    def login_qun_qq_com(self):
        # 登录qun.qq.com

        # 访问网页，为了获取参数pt_login_sig
        login_url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=549000912&s_url=http://qun.qq.com/member.html'
        html = get_html(login_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        pt_login_sig = cookies_back_dict['pt_login_sig']
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)

        # 访问网页，为了获取参数ptqrtoken
        qrcode_url = 'https://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.39550762134604156'
        html = get_html(qrcode_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        qrsig = cookies_back_dict['qrsig']
        ptqrtoken = hash33_token(qrsig)
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)

        # 将登录二维码写到本地，并自动打开，让用户扫描
        with open('qrcode1.png', "wb") as f:
            f.write(html.content)

        # 调用系统默认打开方式，打开该二维码
        open_file_by_system('qrcode1.png')



        # 实时检测二维码状态
        while (True):
            # 目标网址
            target_url = 'http://ptlogin2.qq.com/ptqrlogin?u1=http://qun.qq.com/member.html&' + 'ptqrtoken=' + str(
                ptqrtoken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1499652067577&js_ver=10224&js_type=1&login_sig=' + str(
                pt_login_sig) + '&pt_uistyle=40&aid=549000912&'

            # 登录，需要带上访问cookies
            html = get_html(target_url, self.cookies_merge_dict_in_qun_qq_com)

            # 返回的响应码为200说明二维码没过期
            if (html.status_code):
                if ('二维码未失效' in html.text):
                    print(u'登录qun.qq.com中，当前二维码未失效，请你扫描二维码进行登录')
                elif ('二维码认证' in html.text):
                    print(u'登录qun.qq.com中，扫描成功，正在认证中')
                elif ('登录成功' in html.text):
                    self.is_login = True
                    print(u'登录qun.qq.com中，登录成功')
                    break
                if ('二维码已经失效' in html.text):
                    print(u'登录qun.qq.com中，当前二维码已失效，请重启本软件')
                    exit()

            # 延时
            time.sleep(2)

        # 登录成功后，把返回的cookies合并进去
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)
        # print(u'当前cookies:{}'.format(cookies_merge_dict))

        # 获取此次登录的qq号码
        qq_list = re.findall(r'&uin=(.+?)&service', html.text)
        self.qq_number = qq_list[0]


        # 登录成功后，会返回一个地址，需要对该地址进行访问以便获取新的返回cookies
        startIndex = (html.text).find('http')
        endIndex = (html.text).find('pt_3rd_aid=0')
        url = (html.text)[startIndex:endIndex] + 'pt_3rd_aid=0'

        # 这里需要注意的是，需要禁止重定向，才能正确获得返回的cookies
        html = requests.get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, allow_redirects=False)
        # 把返回的cookies合并进去
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)



    def login_id_qq_com(self):
        # 登录id.qq.com

        # 访问网页，为了获取参数pt_login_sig
        login_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?pt_disable_pwd=1&appid=1006102&daid=1&style=23&hide_border=1&proxy_url=https://id.qq.com/login/proxy.html&s_url=https://id.qq.com/index.html'
        html = get_html(login_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        pt_login_sig = cookies_back_dict['pt_login_sig']
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)

        # 访问网页，为了获取参数ptqrtoken
        qrcode_url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=1006102&e=2&l=M&s=3&d=72&v=4&t=0.10239549811477189&daid=1&pt_3rd_aid=0'
        html = get_html(qrcode_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        qrsig = cookies_back_dict['qrsig']
        ptqrtoken = hash33_token(qrsig)
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)

        # 将登录二维码写到本地，并自动打开，让用户扫描
        with open('qrcode2.png', "wb") as f:
            f.write(html.content)

        # 调用系统默认打开方式，打开该二维码
        open_file_by_system('qrcode2.png')


        # 实时检测二维码状态
        while (True):
            # 目标网址
            target_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https://id.qq.com/index.html&ptqrtoken=' + str(ptqrtoken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1556812236254&js_ver=19042519&js_type=1&login_sig=' + str(pt_login_sig) + '&pt_uistyle=40&aid=1006102&daid=1&'

            # 登录，需要带上访问cookies
            html = get_html(target_url, self.cookies_merge_dict_in_id_qq_com)

            # 返回的响应码为200说明二维码没过期
            if (html.status_code):
                if ('二维码未失效' in html.text):
                    print(u'登录id.qq.com中，当前二维码未失效，请你扫描二维码进行登录')
                elif ('二维码认证' in html.text):
                    print(u'登录id.qq.com中，扫描成功，正在认证中')
                elif ('登录成功' in html.text):
                    self.is_login = True
                    print(u'登录id.qq.com中，登录成功')
                    break
                if ('二维码已经失效' in html.text):
                    print(u'登录id.qq.com中，当前二维码已失效，请重启本软件')
                    exit()

            # 延时
            time.sleep(2)

        # 登录成功后，把返回的cookies合并进去
        self.cookies_merge_dict_in_id_qq_com = requests.utils.dict_from_cookiejar(html.cookies)
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)
        # print(u'当前cookies:{}'.format(cookies_merge_dict))

        # 获取此次登录的qq号码
        qq_list = re.findall(r'&uin=(.+?)&service', html.text)
        self.qq_number = qq_list[0]


        # 登录成功后，会返回一个地址，需要对该地址进行访问以便获取新的返回cookies
        startIndex = (html.text).find('http')
        endIndex = (html.text).find('pt_3rd_aid=0')
        url = (html.text)[startIndex:endIndex] + 'pt_3rd_aid=0'

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()

        # 这里需要注意的是，需要禁止重定向，才能正确获得返回的cookies
        html = requests.get(url, cookies=self.cookies_merge_dict_in_id_qq_com, allow_redirects=False, verify=False)
        # 把返回的cookies合并进去
        cookies_back_dict = requests.utils.dict_from_cookiejar(html.cookies)
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)






    def get_group(self):

        # 获取所有群基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        submit_data = {'bkn': bkn}
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_group_list', self.cookies_merge_dict_in_qun_qq_com, submit_data)
        group_info = json.loads(html.text)
        print(group_info)
        return group_info['join']



    def get_members_in_group(self,group_number):

        # 获取某个群的群成员
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        url = 'http://qinfo.clt.qq.com/cgi-bin/qun_info/get_members_info_v1?friends=1&name=1&gc=' + str(group_number) + '&bkn=' + str(bkn) + '&src=qinfo_v3'
        html = get_html(url, self.cookies_merge_dict_in_qun_qq_com)
        group_member = json.loads(html.text)
        return group_member




    def get_all_friends_in_qq(self):

        # 获取所有qq好友基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        submit_data = {'bkn': bkn}
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_friend_list', self.cookies_merge_dict_in_qun_qq_com, submit_data)
        friend_info = json.loads(html.text)
        # print(friend_info)
        return friend_info['result']




    def get_info_in_qq_friend(self,qq_number):

        # 获取某个qq好友的详细信息

        # 需要提交的数据
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        submit_data = {'keyword':str(qq_number), 'ldw': str(bkn), 'num':'20', 'page':'0', 'sessionid':'0', 'agerg':'0', 'sex':'0', 'firston':'0', 'video':'0', 'country':'1', 'province':'65535', 'city':'0', 'district':'0', 'hcountry':'1', 'hprovince':'0', 'hcity':'0', 'hdistrict':'0', 'online':'0'}

        # 需要提交的cookies
        # cookies = {'uin':self.cookies_merge_dict_in_qun_qq_com['uin'], 'skey':self.cookies_merge_dict_in_qun_qq_com['skey'], 'ptisp':self.cookies_merge_dict_in_qun_qq_com['ptisp'], 'RK':self.cookies_merge_dict_in_qun_qq_com['RK'], 'ptcz':self.cookies_merge_dict_in_qun_qq_com['ptcz']}

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://find.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://find.qq.com/',
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,post方式
        html = requests.post('http://cgi.find.qq.com/qqfind/buddy/search_v3', data=submit_data, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将好友信息解析为python对象
        friend_info = json.loads(html.text)
        # print(friend_info)
        return friend_info['result']['buddy']['info_list'][0]




    def get_profile_picture(self, qq_number, size=100):
        # 获取指定qq的头像，size的值可为40、100、140，默认为100
        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://find.qq.com/'
        }

        # 网页访问,get方式
        # https://q4.qlogo.cn/g?b=qq&nk=10000&s=140
        html = requests.get('https://q4.qlogo.cn/g?b=qq&nk=' + str(qq_number) + '&s=' + str(size), headers=header, verify=False)
        return html.content



    def get_quit_of_group(self):
        # 获取最近30天内退出的群
        # 需要提交的数据
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        submit_data = {'bkn': str(bkn)}

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'text/plain',
            'origin': 'https://huifu.qq.com',
            'referer' : 'https://huifu.qq.com/recovery/index.html?frag=0'
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,post方式
        html = requests.post('https://huifu.qq.com/cgi-bin/gr_grouplist', data=submit_data, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = json.loads(html.text)

        return result


    def get_delete_friend_in_360day(self):

        # 获取最近一年删除的好友名单
        # 需要提交的数据
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        qq_number = str(self.qq_number)
        skey = str(self.cookies_merge_dict_in_qun_qq_com['skey'])
        url = 'https://proxy.vip.qq.com/cgi-bin/srfentry.fcgi?bkn=' + str(bkn) + '&ts=&g_tk=' + str(bkn) + '&data={"11053":{"iAppId":1,"iKeyType":1,"sClientIp":"","sSessionKey":"' + skey + '","sUin":"' + qq_number + '"}}'

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://huifu.qq.com/recovery/index.html?frag=1',
            'Origin': 'https://huifu.qq.com',
            'Connection': 'close'
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,post方式
        html = requests.get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = json.loads(html.text)
        # print(result)

        # 364天内没有删除的好友
        delFriendList = result['11053']['data']['delFriendList']
        if(len(delFriendList) == 0):
            return {}

        # 364天内有删除的好友
        qq_number_list = delFriendList['364']['vecUin']

        # 返回364天内的被删除的好友名单
        return qq_number_list


    def is_vip_svip(self):
        # 判断此次登录的qq是否为vip或者svip
        # 需要提交的数据
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        qq_number = str(self.qq_number)
        skey = str(self.cookies_merge_dict_in_qun_qq_com['skey'])
        url = 'https://proxy.vip.qq.com/cgi-bin/srfentry.fcgi?bkn=' + str(bkn) + '&ts=&g_tk=' + str(bkn) + '&data={"11053":{"iAppId":1,"iKeyType":1,"sClientIp":"","sSessionKey":"' + skey + '","sUin":"' + qq_number + '"}}'

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://huifu.qq.com/recovery/index.html?frag=1',
            'Origin': 'https://huifu.qq.com',
            'Connection': 'close'
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,post方式
        html = requests.get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = json.loads(html.text)
        isSvip = result['11053']['data']['isSvip']
        isVip = result['11053']['data']['isVip']
        return {'isSvip':isSvip, 'isVip':isVip}


    def get_qb(self):
        # 获取该账户的qb值
        # 需要提交的数据
        qq_number = str(self.qq_number)
        skey = str(self.cookies_merge_dict_in_qun_qq_com['skey'])
        url = 'https://api.unipay.qq.com/v1/r/1450000186/wechat_query?cmd=4&pf=vip_m-pay_html5-html5&pfkey=pfkey&from_h5=1&from_https=1&openid=' + qq_number + '&openkey=' + skey + '&session_id=uin&session_type=skey'

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://my.pay.qq.com/account/index.shtml',
            'Connection': 'keep-alive'
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,get方式
        html = requests.get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = json.loads(html.text)

        qb_value = float(result['qb_balance']) / 100
        return qb_value


    def get_pay_for_another(self):
        # 获取帮别人的代付
        # 需要提交的数据
        skey = str(self.cookies_merge_dict_in_qun_qq_com['skey'])
        url = 'https://pay.qq.com/cgi-bin/personal/account_msg.cgi?p=0.6796416908412624&cmd=1&sck=' + get_sck(skey) + '&type=100&showitem=2&per=100&pageno=1&r=0.3177912609760205'

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://pay.qq.com/infocenter/infocenter.shtml?asktype=100',
            'Connection': 'keep-alive'
        }

        # 屏蔽https证书警告
        requests.packages.urllib3.disable_warnings()
        # 网页访问,get方式
        html = requests.get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = json.loads(html.text)
        # print(result)

        return result['resultinfo']['list']




