# -*- coding:utf-8 -*-

# 引用自定义库
from qq_bot import *
from static_data import *

# 引用第三方库
from threading import Thread
from os.path import exists
from os import makedirs
from shutil import rmtree
from base64 import b64decode
import time


# 初始化所需文件夹
def init_folders():

    for dir in ['data']:
        if(not (exists(dir))):
            # 目录不存在时则创建
            makedirs(dir)
        else:
            # 目录存在时则先删除递归删除该目录再重新创建
            rmtree(dir)
            makedirs(dir)


# 写入相关资源文件到本地
def write_data():

    key_dict = {
        'qq_icon':qq_icon,
        'level_star':level_star,
        'level_moon':level_moon,
        'level_sun':level_sun,
        'level_crown':level_crown
    }
    for name in ['qq_icon', 'level_star', 'level_moon', 'level_sun', 'level_crown']:
        # 保存qq_icon图片到本地data目录
        with open('data/' + name + '.png', 'wb') as file:
            # 解码图片
            png = b64decode(key_dict[name])
            # 将解码得到的数据写入到图片中
            file.write(png)


# 根据Q等级绘制等级图标
def calculate_level(level):
    level = int(level)
    star_count = 0
    moon_count = 0
    sun_count = 0
    crown_count = 0

    # //表示向下取整 %表示取余
    crown_count = level // 64
    tmp = level % 64

    sun_count = tmp // 16
    tmp = tmp % 16

    moon_count = tmp // 4
    tmp = tmp % 4

    star_count = tmp // 1

    return star_count, moon_count, sun_count, crown_count


# 获取个人数据
def generate_data():

    # 定义欲输出的markdown字符串
    markdown_content = '''
<p align="center">
    <font size='6px'>{qq_number}的个人QQ历史报告</font>
    <img src="{qq_icon_png}" align="right" height="60">
</p>
'''

    # 初始化文件夹
    init_folders()
    # 写入项目所需资源文件到本地目录
    write_data()




    # 创建一个自己编写的qq bot对象
    bot = Bot()
    custom_print(u'登录成功!')
    # 更新一下欲输出的markdown文本
    markdown_content = markdown_content.replace('{qq_number}',bot.qq_number)
    markdown_content = markdown_content.replace('{qq_icon_png}', 'data/qq_icon.png')




    # 获取该登录账户的详细资料
    custom_print(u'正在获取该账户的个人数据...')
    detail_information = bot.get_detail_information()
    # content为markdown语法文本
    content = '\n<br/><br/>\n' + '## 我的详细资料\n' + '种类|内容\n:- | :-\n'

    # 将key换成中文文本
    key_dict = {
        'bind_email':'绑定邮箱',
        'last_contact_friend_count': '最近联系人数量',
        'friend_count': '好友数量',
        'group_count': '好友分组数量',
        'qq_level': '账号等级',
        'qq_level_rank': '等级排名',
        'nickname': '昵称',
        'odd_friend_count': '**单向好友数量**',
        'qq_age': 'Q龄',
        'remark_friend_count':'已备注的好友数量',
        'mobile_qq_online_hour': '**手机QQ累计在线时间(小时)**',
        'no_hide_online_hour': '**未隐身状态下累计在线时间(小时)**',
        'total_active_day': '**在线活跃时间**',
        'age': '真实年龄',
        'birthday': '出生日期',
        'qq_signature': '个性签名(前20字)',
    }

    for key, value in detail_information.items():
        if key == 'qq_level':
            star_count, moon_count, sun_count, crown_count = calculate_level(value)
            data = crown_count * '![](data/level_crown.png)' + sun_count * '![](data/level_sun.png)' + moon_count * '![](data/level_moon.png)' + star_count * '![](data/level_star.png)'
            content += '{}|{}\n'.format(key_dict[key], data)
        else:
            content += '{}|{}\n'.format(key_dict[key], value)
    # 更新一下欲输出的markdown文本
    markdown_content += content
    markdown_content += '\n> 注：单向好友表示他/她的列表中有你，而你的列表中没有他/她'
    # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)



    # 获取所有好友列表接口已失效
    '''
    # 获取所有qq好友的备注名和qq号
    custom_print(u'正在获取该账户的好友数据...')
    all_qq_friends = bot.get_all_friends_in_qq() # 获取所有好友列表接口已失效
    qq_number_list = []
    for key, friend_group in all_qq_friends.items():
        for info in friend_group['mems']:
            qq_number_list.append(info['uin'])
    '''



    # 获取所有群信息
    custom_print(u'正在获取该账户的所有群信息...')
    group_list = bot.get_group()
    # content为markdown语法文本
    content = '\n\n<br/><br/>\n' + '## 我加入的群资料\n' + '序号|群名|群号|群主QQ\n:- | :-| :-| :-\n'
    # 获取某个群的群成员信息
    for index, group in enumerate(group_list):
        group_number = group['gc']
        group_name = group['gn']
        owner = group['owner']
        content += '{}|{}|{}|{}\n'.format(str(index+1), str(group_name), str(group_number), str(owner))

    # 更新一下欲输出的markdown文本
    markdown_content += content
    # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)





    # 获取过去30天内退出的群名单
    custom_print(u'正在获取该账户过去30天退出的群...')
    data = bot.get_quit_of_group()
    delete_group_count = 0
    # content为markdown语法文本
    content = '\n\n<br/><br/>\n' + '## 过去30天内我退出的群\n'
    if 'ls' in data.keys():
        delete_group_count = len(data['ls'])
    content += '过去30天内，我退出的群个数为**{}**个'.format(delete_group_count)

    if(delete_group_count > 0):
        content += '，它们分别是：\n' + '序号|群名|群号|退出时间\n:- | :-| :-| :-\n'
        for index, group in enumerate(data['ls']):
            timeStamp = int(group['t'])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

            content += '{}|{}|{}|{}\n'.format(str(index),group['n'],group['gc'],otherStyleTime)

    content += '\n\n'
    # 更新一下欲输出的markdown文本
    markdown_content += content
    # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)






    # 获取过去364天内删除的好友名单
    custom_print(u'正在获取该账户过去12个月删除的好友名单...')
    delete_friend_list = bot.get_delete_friend_in_360day()
    delete_friend_count = len(delete_friend_list)
    # content为markdown语法文本
    content = '\n\n<br/><br/>\n' + '## 过去364天内我删除的好友\n'
    content += '过去364天内，我删除的好友个数为**{}**个'.format(delete_friend_count)
    if(delete_friend_count > 0):
        content += '，它们分别是：\n' + '序号|Q号\n:- | :-\n'
        for index, qq_number in enumerate(delete_friend_list):
            content += '{}|{}\n'.format(str(index),str(qq_number))

    content += '\n\n'
    # 更新一下欲输出的markdown文本
    markdown_content += content
    # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)








    # 判断此次登录的qq是否为vip或者svip
    # content为markdown语法文本
    content = '\n\n<br/><br/>\n' + '## 财产分析\n'
    custom_print(u'正在判断该账户是否为VIP...')
    data = bot.is_vip_svip()
    isSvip = data['isSvip']
    isVip = data['isSvip']
    if(str(isVip) == '0' and str(isSvip) == '0'):
        content += '此时此刻，我既不是**QQ VIP**，也不是**QQ SVIP**\n'
    elif(str(isVip) != '0' and str(isSvip) != '0'):
        content += '此时此刻，我既是**QQ VIP**，也是**QQ SVIP**\n'
    elif(str(isVip) == '0' and str(isSvip) != '0'):
        content += '此时此刻，我不是**QQ VIP**，但我是**QQ SVIP**\n'
    elif(str(isVip) != '0' and str(isSvip) == '0'):
        content += '此时此刻，我是**QQ VIP**，但不是**QQ SVIP**\n'

    # 获取qb值
    custom_print(u'正在获取该账户的Q币...')
    qb_value = bot.get_qb()
    timeArray = time.localtime()
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    content += '截止到**{}**，我剩余的Q币个数为：**{}**个\n\n'.format(otherStyleTime,qb_value)

    # 获取代付信息
    custom_print(u'正在获取该账户的代付信息...')
    pay_list = bot.get_pay_for_another()
    content += '截止到**{}**，我收到的代付信息条数为：**{}**个'.format(otherStyleTime, len(pay_list))
    if(len(pay_list) > 0):
        content += '，它们分别是：\n' + '序号|索要者QQ|索要者昵称|留言内容|索要时间\n:- | :-| :-| :-| :-\n'
        for index, pay_info in enumerate(pay_list):
            if(str(pay_info['fromuin']) != '0'):
                nick = pay_info['nick'].replace('&nbsp;',' ')
                timeArray = time.localtime(int(pay_info['trantime']))
                otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
                content += '{}|{}|{}|{}|{}\n'.format(str(index),str(pay_info['fromuin']),nick,str(pay_info['content']),otherStyleTime)

    content += '\n\n'
    # 更新一下欲输出的markdown文本
    markdown_content += content
    # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)





    # 亲密度排行榜 谁在意我
    custom_print(u'正在分析好友亲密度数据-谁在意我...')
    # content为markdown语法文本
    content = '\n\n<br/><br/>\n' + '## 谁在意我\n'
    data_list = bot.who_care_about_me()
    n = 10
    if(len(data_list) < 10):
        n = len(data_list)

    if (len(data_list) > 0):
        content += '序号|头像|昵称|QQ|亲密度\n:- | :-| :-| :-\n'
        for index, sub_data in enumerate(data_list[:n]):
            uin = sub_data['uin']
            score = sub_data['score']
            name = sub_data['name']
            profile = bot.get_profile_picture(uin, size=40)
            with open('data/' + str(uin) + '.jpg', 'wb') as f:
                f.write(profile)
            content += '{}|![](data/{}.jpg)|{}|{}|{}\n'.format(index, uin, name, uin, score)

        # 更新一下欲输出的markdown文本
        markdown_content += content
        # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
        with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
            file.write(markdown_content)





    # 亲密度排行榜 我在意谁
    custom_print(u'正在分析好友亲密度数据-我在意谁...')
    # content为markdown语法文本
    content = '\n\n<br/><br/>\n' + '## 我在意谁\n'
    data_list = bot.i_care_about_who()
    n = 10
    if(len(data_list) < 10):
        n = len(data_list)

    if (len(data_list) > 0):
        content += '序号|头像|昵称|QQ|亲密度\n:- | :-| :-| :-\n'
        for index, sub_data in enumerate(data_list[:n]):
            uin = sub_data['uin']
            score = sub_data['score']
            name = sub_data['name']
            profile = bot.get_profile_picture(uin, size=40)
            with open('data/' + str(uin) + '.jpg', 'wb') as f:
                f.write(profile)
            content += '{}|![](data/{}.jpg)|{}|{}|{}\n'.format(index, uin, name, uin, score)

        # 更新一下欲输出的markdown文本
        markdown_content += content
        # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
        with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
            file.write(markdown_content)



    # 每个步骤完成后，保存markdown文件，以便防止程序出错时能够保存到最新的数据
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)

    custom_print(u'所有数据获取完毕, 并在当前工作目录下生成了一份报告文件:[{}的个人QQ历史报告.md]'.format(bot.qq_number))
    custom_print(u'该文件为markdown格式, 请下载typora软件以便查看该文件, 下载地址为https://typora.io/')

if __name__ == "__main__":


    # 启动获取数据线程
    t = Thread(target=generate_data, name='generate_data')
    t.start()

    # 启动tkinter gui
    gui()
