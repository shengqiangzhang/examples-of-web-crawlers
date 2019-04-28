# -*- coding:utf-8 -*-

# 引用自定义库
from qq_group import QQGroup
import element_encrypt


# 引用第三方库
import time
import random










if __name__ == "__main__":

    # 创建一个群对象
    qq_group = QQGroup()

    # # 获取群信息
    # group_dict = qq_group.get_group()
    # print(group_dict)
    #
    #
    # # 获取某个群的群成员信息
    # for group in group_dict:
    #     print(qq_group.get_members_in_group(str(group['gc'])))
    #     # 经测试，频繁获取将会被封该功能，正在解决
    #     time.sleep(5)
    #
    #
    # # 获取所有qq好友的备注名和qq号
    # print(qq_group.get_all_friends_in_qq())
    #
    # # 查找指定qq详细信息
    # print(qq_group.get_info_in_qq_friend(10000))



    # 获取指定qq的头像
    qq_group.get_profile_picture(10000)

    # qq推广https://shang.qq.com/v3/index.html
    # qq个人中心https://id.qq.com/index.html#index
    # 亲密度排行榜 https://rc.qzone.qq.com/myhome/friends
    # 近期加你好友的人 https://rc.qzone.qq.com/myhome/friends/center
    # 成为QQ好友的天数https://user.qzone.qq.com/981469881/friendship?via=ic
    # 成为qq好友的天数https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/friendship/cgi_friendship?activeuin=3257179914&passiveuin=928255652&situation=1&isCalendar=1&g_tk=138378367&qzonetoken=8b160efd39b85efd4ffeba1a4f8501c063e6ff850976285b9f5f6d20cafc8163b55db14b65ce4f2edb5c&g_tk=138378367
    # 最近一年删除的好友或者退群的数量https://huifu.qq.com/recovery/index.html?frag=1


