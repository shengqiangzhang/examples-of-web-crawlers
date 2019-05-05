# -*- coding:utf-8 -*-

# 引用自定义库
from qq_bot import *

# 引用第三方库
from threading import Thread
from os.path import exists
from os import makedirs
from shutil import rmtree


# 初始化所需文件夹
def init_folders():
    if(not (exists('image'))):
        makedirs('image')
    else:
        rmtree('image')
        makedirs('image')


# 获取个人数据
def generate_data():
    # 经测试，所有接口如果调用过于频繁，将被禁止获取该接口12小时，建议加上延迟time.sleep(1)

    # 创建一个群对象
    bot = Bot()

    # 获取该账户的详细资料
    a = bot.get_detail_information()
    custom_print(str(a))

    # 获取群信息
    custom_print(u'获取该QQ加入的所有群信息...')
    group_list = bot.get_group()
    custom_print(u'获取该QQ加入的所有群信息完毕')

    # 获取某个群的群成员信息
    custom_print(u'获取该该群的成员信息...')
    bot.get_members_in_group(str(group_list[0]['gc']))
    custom_print(u'获取该该群的成员信息完毕')

    # 获取所有qq好友的备注名和qq号
    all_qq_friends = bot.get_all_friends_in_qq()
    print('所有qq好友号码和备注名',all_qq_friends)

    # 查找指定qq详细信息
    custom_print(u'获取该QQ的详细资料...')
    bot.get_info_in_qq_friend(bot.qq_number)
    custom_print(u'获取该QQ的详细资料完毕')

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






if __name__ == "__main__":
    # 启动获取数据线程
    t = Thread(target=generate_data, name='generate_data')
    t.start()

    # 绘制gui
    main_gui = gui()



