# -*- coding:utf-8 -*-

# 引用自定义库
from qq_bot import *
from static_data import *

# 引用第三方库
from threading import Thread
from os.path import exists
from os import makedirs
from shutil import rmtree
import base64


# 初始化所需文件夹
def init_folders():

    for dir in ['image', 'data']:
        if(not (exists(dir))):
            # 目录不存在时则创建
            makedirs(dir)
        else:
            # 目录存在时则先删除递归删除该目录再重新创建
            rmtree(dir)
            makedirs(dir)


# 写入资源文件到本地
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
            png = base64.b64decode(key_dict[name])
            # 将解码得到的数据写入到图片中
            file.write(png)



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
    custom_print(u'登录成功,正在获取数据...')
    # 更新一下欲输出的markdown文本
    markdown_content = markdown_content.replace('{qq_number}',bot.qq_number)
    markdown_content = markdown_content.replace('{qq_icon_png}', 'data/qq_icon.png')






    # 获取该登录账户的详细资料
    custom_print(u'正在获取该登录账户的详细数据...')
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
        content += '{}|{}\n'.format(key_dict[key], value)
    # 更新一下欲输出的markdown文本
    markdown_content += content
    markdown_content += '\n> 注：单向好友表示他/她的列表中有你，而你的列表中没有他/她'





    # 获取群信息
    custom_print(u'获取该QQ加入的所有群信息...')
    group_list = bot.get_group()
    custom_print(u'获取该QQ加入的所有群信息完毕')

    # 获取某个群的群成员信息
    custom_print(u'获取该该群的成员信息...')
    bot.get_members_in_group(str(group_list[0]['gc']))
    custom_print(u'获取该该群的成员信息完毕')

    # 获取所有qq好友的备注名和qq号
    # Bot对象中含有查询指定qq好友详细资料的接口
    # 但是由于该接口限制十分严格，频繁获取超过10个以上会封该QQ号码12小时
    # 所以放弃对每个好友详细资料的分析
    all_qq_friends = bot.get_all_friends_in_qq()
    print('所有qq好友号码和备注名',all_qq_friends)


    # 获取过去30天内退出的群名单
    custom_print(u'获取过去30天退出的群...')
    print('过去30天内退出的群',bot.get_quit_of_group())
    custom_print(u'获取过去30天退出的群完毕')

    # 获取过去364天内删除的好友名单
    custom_print(u'获取过去12个月删除的好友名单...')
    bot.get_delete_friend_in_360day()
    custom_print(u'获取过去12个月删除的好友名单完毕')


    # 判断此次登录的qq是否为vip或者svip
    custom_print(u'判断该QQ是否为高级用户...')
    bot.is_vip_svip()
    custom_print(u'判断完毕')







    # # 获取指定qq的头像
    #
    # # 初始化存放头像文件夹
    # init_folders()
    # # 生成qq-备注名字典
    # qq_name_dict = {}
    # for group in all_qq_friends.keys():
    #     for info in all_qq_friends[group]['mems']:
    #         qq_name_dict.update({info['uin']:info['name']})
    # # 开始下载qq头像
    # for index,qq_number in enumerate(qq_name_dict.keys()):
    #     image = bot.get_profile_picture(qq_number)
    #     with open('image/' + str(qq_number) + '.jpg', 'wb') as f:
    #         f.write(image)
    #     print('{}/{}'.format(index + 1, len(qq_name_dict)))



    # 获取qb值
    custom_print(u'获取账户QB值...')
    bot.get_qb()
    custom_print(u'获取账户QB值完毕')


    # 获取代付信息
    custom_print(u'获取代付信息中...')
    bot.get_pay_for_another()
    custom_print(u'获取代付信息完毕')



    # qq音乐以前空间上传的歌单


    # qq个人中心https://id.qq.com/index.html#index
    # 亲密度排行榜 https://rc.qzone.qq.com/myhome/friends
    # 近期加你好友的人 https://rc.qzone.qq.com/myhome/friends/center
    # 成为QQ好友的天数https://user.qzone.qq.com/981469881/friendship?via=ic
    # 成为qq好友的天数https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/friendship/cgi_friendship?activeuin=3257179914&passiveuin=928255652&situation=1&isCalendar=1&g_tk=138378367&qzonetoken=8b160efd39b85efd4ffeba1a4f8501c063e6ff850976285b9f5f6d20cafc8163b55db14b65ce4f2edb5c&g_tk=138378367


    # 输出markdown文件
    with open('{}的个人QQ历史报告.md'.format(bot.qq_number), 'w', encoding='utf-8') as file:
        file.write(markdown_content)

if __name__ == "__main__":

    # 启动获取数据线程
    t = Thread(target=generate_data, name='generate_data')
    t.start()

    # 启动tkinter gui
    gui()


