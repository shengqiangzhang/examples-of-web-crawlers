# -*- coding:utf-8 -*-

# 引用自定义库
from qq_bot import Bot


if __name__ == "__main__":

    # 经测试，所有接口如果调用过于频繁，将被禁止获取该接口12小时，建议加上延迟time.sleep(1)


    # 创建一个群对象
    bot = Bot()

    # 获取群信息
    group_list = bot.get_group()
    print('所有群:',group_list)

    # 获取某个群的群成员信息
    print('某个群的成员信息',bot.get_members_in_group(str(group_list[0]['gc'])))

    # 获取所有qq好友的备注名和qq号
    all_qq_friends = bot.get_all_friends_in_qq()
    print('所有qq好友号码和备注名',all_qq_friends)

    # 查找指定qq详细信息
    print('某个qq的详细信息', bot.get_info_in_qq_friend(3257179914))

    # 获取过去30天内退出的群名单
    print('过去30天内退出的群',bot.get_quit_of_group())

    # 获取过去364天内删除的好友名单
    print('过去12个月删除的好友', bot.get_delete_friend_in_360day())

    # 判断此次登录的qq是否为vip或者svip
    print('是否为vip或者svip',bot.is_vip_svip())

    # 获取指定qq的头像
    # image = bot.get_profile_picture(3257179914)
    # with open(str(3257179914) + '.jpg', 'wb') as f:
    #     f.write(image)



    # 获取qb值
    print('qb值',bot.get_qb())

    # 获取代付信息
    print('查询代付信息',bot.get_pay_for_another())


    # qq音乐以前空间上传的歌单


    # qq个人中心https://id.qq.com/index.html#index
    # 亲密度排行榜 https://rc.qzone.qq.com/myhome/friends
    # 近期加你好友的人 https://rc.qzone.qq.com/myhome/friends/center
    # 成为QQ好友的天数https://user.qzone.qq.com/981469881/friendship?via=ic
    # 成为qq好友的天数https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/friendship/cgi_friendship?activeuin=3257179914&passiveuin=928255652&situation=1&isCalendar=1&g_tk=138378367&qzonetoken=8b160efd39b85efd4ffeba1a4f8501c063e6ff850976285b9f5f6d20cafc8163b55db14b65ce4f2edb5c&g_tk=138378367

