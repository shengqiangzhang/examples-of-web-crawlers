# -*- coding:utf-8 -*-

# 引用自定义库
from encrypt import hash33_token
from encrypt import hash33_bkn
from encrypt import get_sck
from url_request import get_html
from url_request import post_html
from encrypt import get_csrf_token


# 引用第三方库
import re
import time
from requests import get
from requests import post
from requests.packages import urllib3
from requests.utils import dict_from_cookiejar
from json import loads
from platform import system
from tkinter import *
from PIL import Image,ImageTk
from io import BytesIO


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
# 用于显示图片的对象
image = ''

# 自定义输出数据
def custom_print(data):
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
        self.image = image
        self.frame = frame
        self.text = text
        self.scroll = scroll

        # 设置禁止调整窗口大小
        root.resizable(False, False)
        # 设置窗口标题
        root.title('一键生成qq个人数据报告')
        # 设置窗口大小及其位置
        self.center_window(800, 160)

        # 设置图像框
        # qr_code = Image.open('qrcode2.png')
        # image = ImageTk.PhotoImage(qr_code)
        # image_label['image'] = image
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

        # 登录成功后，将QQ头像显示到图片框
        picture = self.get_profile_picture(self.qq_number,140)
        BytesIOObj = BytesIO()
        BytesIOObj.write(picture)
        qr_code = Image.open(BytesIOObj)
        global image
        image = ImageTk.PhotoImage(qr_code)
        image_label['image'] = image





    def login_qun_qq_com(self):
        # 登录qun.qq.com

        # 访问网页，为了获取参数pt_login_sig
        login_url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=549000912&s_url=http://qun.qq.com/member.html'
        html = get_html(login_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = dict_from_cookiejar(html.cookies)
        pt_login_sig = cookies_back_dict['pt_login_sig']
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)

        # 访问网页，为了获取参数ptqrtoken
        qrcode_url = 'https://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=4&d=72&v=4&t=0.39550762134604156'
        html = get_html(qrcode_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = dict_from_cookiejar(html.cookies)
        qrsig = cookies_back_dict['qrsig']
        ptqrtoken = hash33_token(qrsig)
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)

        # 将二维码显示到图片框
        BytesIOObj = BytesIO()
        BytesIOObj.write(html.content)
        qr_code = Image.open(BytesIOObj)
        global image
        image = ImageTk.PhotoImage(qr_code)
        image_label['image'] = image



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
                    custom_print(u'登录qun.qq.com中，当前二维码未失效，请你扫描二维码进行登录')
                elif ('二维码认证' in html.text):
                    custom_print(u'登录qun.qq.com中，扫描成功，正在认证中')
                elif ('登录成功' in html.text):
                    self.is_login = True
                    custom_print(u'登录qun.qq.com中，登录成功')
                    break
                if ('二维码已经失效' in html.text):
                    custom_print(u'登录qun.qq.com中，当前二维码已失效，请重启本软件')
                    exit()

            # 延时
            time.sleep(2)

        # 登录成功后，把返回的cookies合并进去
        cookies_back_dict = dict_from_cookiejar(html.cookies)
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
        html = get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, allow_redirects=False)
        # 把返回的cookies合并进去
        cookies_back_dict = dict_from_cookiejar(html.cookies)
        self.cookies_merge_dict_in_qun_qq_com.update(cookies_back_dict)



    def login_id_qq_com(self):
        # 登录id.qq.com

        # 访问网页，为了获取参数pt_login_sig
        login_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?pt_disable_pwd=1&appid=1006102&daid=1&style=23&hide_border=1&proxy_url=https://id.qq.com/login/proxy.html&s_url=https://id.qq.com/index.html'
        html = get_html(login_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = dict_from_cookiejar(html.cookies)
        pt_login_sig = cookies_back_dict['pt_login_sig']
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)

        # 访问网页，为了获取参数ptqrtoken
        qrcode_url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=1006102&e=2&l=M&s=4&d=72&v=4&t=0.10239549811477189&daid=1&pt_3rd_aid=0'
        html = get_html(qrcode_url, '')
        # 对返回的cookies进行转化为dict类型，方便处理
        cookies_back_dict = dict_from_cookiejar(html.cookies)
        qrsig = cookies_back_dict['qrsig']
        ptqrtoken = hash33_token(qrsig)
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)


        # 将二维码显示到图片框
        BytesIOObj = BytesIO()
        BytesIOObj.write(html.content)
        qr_code = Image.open(BytesIOObj)
        global image
        image = ImageTk.PhotoImage(qr_code)
        image_label['image'] = image


        # 实时检测二维码状态
        while (True):
            # 目标网址
            target_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https://id.qq.com/index.html&ptqrtoken=' + str(ptqrtoken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1556812236254&js_ver=19042519&js_type=1&login_sig=' + str(pt_login_sig) + '&pt_uistyle=40&aid=1006102&daid=1&'

            # 登录，需要带上访问cookies
            html = get_html(target_url, self.cookies_merge_dict_in_id_qq_com)

            # 返回的响应码为200说明二维码没过期
            if (html.status_code):
                if ('二维码未失效' in html.text):
                    custom_print(u'登录id.qq.com中，当前二维码未失效，请你扫描二维码进行登录')
                elif ('二维码认证' in html.text):
                    custom_print(u'登录id.qq.com中，扫描成功，正在认证中')
                elif ('登录成功' in html.text):
                    self.is_login = True
                    custom_print(u'登录id.qq.com中，登录成功')
                    break
                if ('二维码已经失效' in html.text):
                    custom_print(u'登录id.qq.com中，当前二维码已失效，请重启本软件')
                    exit()

            # 延时
            time.sleep(2)

        # 登录成功后，把返回的cookies合并进去
        self.cookies_merge_dict_in_id_qq_com = dict_from_cookiejar(html.cookies)
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
        urllib3.disable_warnings()

        # 这里需要注意的是，需要禁止重定向，才能正确获得返回的cookies
        html = get(url, cookies=self.cookies_merge_dict_in_id_qq_com, allow_redirects=False, verify=False)
        # 把返回的cookies合并进去
        cookies_back_dict = dict_from_cookiejar(html.cookies)
        self.cookies_merge_dict_in_id_qq_com.update(cookies_back_dict)





    def get_group(self):

        # 获取所有群基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        submit_data = {'bkn': bkn}
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_group_list', self.cookies_merge_dict_in_qun_qq_com, submit_data)
        group_info = loads(html.text)
        # print(group_info)
        return group_info['join']



    def get_members_in_group(self,group_number):

        # 获取某个群的群成员
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        url = 'http://qinfo.clt.qq.com/cgi-bin/qun_info/get_members_info_v1?friends=1&name=1&gc=' + str(group_number) + '&bkn=' + str(bkn) + '&src=qinfo_v3'
        html = get_html(url, self.cookies_merge_dict_in_qun_qq_com)
        group_member = loads(html.text)
        return group_member




    def get_all_friends_in_qq(self):

        # 获取所有qq好友基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_qun_qq_com['skey'])
        submit_data = {'bkn': bkn}
        html = post_html('https://qun.qq.com/cgi-bin/qun_mgr/get_friend_list', self.cookies_merge_dict_in_qun_qq_com, submit_data)
        friend_info = loads(html.text)
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
        urllib3.disable_warnings()
        # 网页访问,post方式
        html = post('http://cgi.find.qq.com/qqfind/buddy/search_v3', data=submit_data, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将好友信息解析为python对象
        friend_info = loads(html.text)
        # print(friend_info)
        return friend_info['result']['buddy']['info_list'][0]




    def get_profile_picture(self, qq_number, size=100):
        # 获取指定qq的头像，size的值可为40、100、140，默认为100
        # 屏蔽https证书警告
        urllib3.disable_warnings()

        # 设置请求头,模拟人工
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://find.qq.com/'
        }

        # 网页访问,get方式
        html = get('http://q1.qlogo.cn/g?b=qq&nk=' + str(qq_number) + '&s=' + str(size), headers=header, verify=False)
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
        urllib3.disable_warnings()
        # 网页访问,post方式
        html = post('https://huifu.qq.com/cgi-bin/gr_grouplist', data=submit_data, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = loads(html.text)

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
        urllib3.disable_warnings()
        # 网页访问,post方式
        html = get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = loads(html.text)
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
        urllib3.disable_warnings()
        # 网页访问,post方式
        html = get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = loads(html.text)
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
        urllib3.disable_warnings()
        # 网页访问,get方式
        html = get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = loads(html.text)

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
        urllib3.disable_warnings()
        # 网页访问,get方式
        html = get(url, cookies=self.cookies_merge_dict_in_qun_qq_com, headers=header, verify=False)

        # 将返回数据解析为python对象
        result = loads(html.text)
        # print(result)

        return result['resultinfo']['list']




    def get_detail_information(self):
        # 获取该账户的详细资料

        # 存储返回数据
        result = {}

        # 获取基本信息
        # bkn由参数skey通过另一个加密函数得到
        bkn = hash33_bkn(self.cookies_merge_dict_in_id_qq_com['skey'])
        url = 'https://id.qq.com/cgi-bin/summary?ldw=' + str(bkn)

        # 设置请求头,模拟人工
        header = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Referer': 'https://id.qq.com/home/home.html?ver=10049&',
            'Connection': 'keep-alive'
        }

        # 屏蔽https证书警告
        urllib3.disable_warnings()
        # 网页访问,get方式
        html = get(url, cookies=self.cookies_merge_dict_in_id_qq_com, headers=header, verify=False)
        # 指定返回数据编码格式
        html.encoding = 'utf-8'
        # 将返回数据解析为python对象，并存入result
        result.update(loads(html.text))




        # 获取在线天数
        skey = str(self.cookies_merge_dict_in_id_qq_com['skey'])
        g_tk = str(get_csrf_token(skey))
        url = 'https://cgi.vip.qq.com/querygrow/get?r=0.8102122812749504&g_tk=' + g_tk
        # 设置请求头,模拟人工
        header = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Referer': 'https://id.qq.com/level/mylevel.html?ver=10043&',
            'Connection': 'keep-alive'
        }
        # 屏蔽https证书警告
        urllib3.disable_warnings()
        # 网页访问,get方式
        html = get(url, cookies=self.cookies_merge_dict_in_id_qq_com, headers=header, verify=False)
        # 指定返回数据编码格式
        html.encoding = 'utf-8'
        # 将返回数据解析为python对象，并存入result
        result.update(loads(html.text))



        # 获取更加详细的资料
        while(True):
            url = 'https://id.qq.com/cgi-bin/userinfo?ldw=' + str(bkn)
            # 设置请求头,模拟人工
            header = {
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Referer': 'https://id.qq.com/myself/myself.html?ver=10045&',
                'Connection': 'keep-alive'
            }
            # 屏蔽https证书警告
            urllib3.disable_warnings()
            # 网页访问,get方式
            html = get(url, cookies=self.cookies_merge_dict_in_id_qq_com, headers=header, verify=False)
            # 指定返回数据编码格式
            html.encoding = 'utf-8'

            # 该网站有时候会返回空数据，所以要判断一下，如果是空则重新发包获取
            if(html.text != ''):
                # 将返回数据解析为python对象，并存入result
                result.update(loads(html.text))

                # 跳出循环
                break


        # 数据获取完毕，筛选出我们想返回的结果
        data = {}
        data.update({'bind_email':result['bind_email']})
        data.update({'last_contact_friend_count': result['chat_count']})
        data.update({'friend_count': result['friend_count']})
        data.update({'group_count': result['group_count']})
        data.update({'qq_level': result['level']})
        data.update({'qq_level_rank': result['level_rank']})
        data.update({'nickname': result['nick']})
        data.update({'odd_friend_count': result['odd_count']})
        data.update({'qq_age': result['qq_age']})
        data.update({'remark_friend_count': result['remark_count']})
        data.update({'mobile_qq_online_hour': result['iMobileQQOnlineTime']})
        data.update({'no_hide_online_hour': result['iNoHideOnlineTime']})
        data.update({'total_active_day': result['iTotalActiveDay']})
        data.update({'age': result['age']})
        data.update({'bir_d': result['bir_d']})
        data.update({'bir_m': result['bir_m']})
        data.update({'bir_y': result['bir_y']})
        qq_signature = result['ln'].replace('&nbsp;',' ')
        data.update({'qq_signature': qq_signature})

        return data

