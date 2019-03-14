from __future__ import unicode_literals
import time
import platform

from wxpy import *
import requests

# 获取每日励志精句
def get_message():
    r = requests.get("http://open.iciba.com/dsapi/")
    note = r.json()['note']
    content = r.json()['content']
    return note,content


# 发送消息给她
def send_message(your_message):
    try:
        # 对方的微信名称
        my_friend = bot.friends().search(my_lady_wechat_name)[0]

        # 发送消息给对方
        my_friend.send(your_message)
    except:

        # 你的微信名称
        my_friend = bot.friends().search(my_wechat_name)[0]

        # 提示
        my_friend.send(u"守护女友出问题了，赶紧去看看咋回事~")



# 在规定时间内进行关心她操作
def start_care():

    # 标志位，防止同一时间内重复发送消息给她
    first_say_good_morning = False
    first_say_good_lunch = False
    first_say_good_dinner = False
    first_say_good_dream = False

    # 待发送的内容，先置为空
    message = ""

    # 来个死循环，24小时关心她
    while(True):

        # 提示
        print("守护中，时间:%s"% time.ctime())

        # 获取时间，只获取时和分，对应的位置为倒数第13位到倒数第8位
        now_time = time.ctime()[-13:-8]

        if (now_time == say_good_morning):
            if(first_say_good_morning == False):
                message = str_good_morning
                send_message(message)
                first_say_good_morning = True
                first_say_good_lunch = False
                first_say_good_dinner = False
                first_say_good_dream = False
                print("提醒女友早上起床:%s" % time.ctime())

        elif (now_time == say_good_lunch):
            if (first_say_good_lunch == False):
                message = str_good_lunch
                send_message(message)
                first_say_good_morning = False
                first_say_good_lunch = True
                first_say_good_dinner = False
                first_say_good_dream = False
                print("提醒女友中午吃饭:%s" % time.ctime())

        elif (now_time == say_good_dinner):
            if (first_say_good_dinner == False):
                message = str_good_dinner
                send_message(message)
                first_say_good_morning = False
                first_say_good_lunch = False
                first_say_good_dinner = True
                first_say_good_dream = False
                print("提醒女友晚上吃饭:%s" % time.ctime())

        elif (now_time == say_good_dream):
            if (first_say_good_dream == False):
                note,content = get_message()
                message = str_good_dream + "\n\n" + "顺便一起来学英语哦：\n" + "原文: " + content + "\n\n翻译: " + note + "\n\n" + "晚安么么哒~"
                send_message(message)
                first_say_good_morning = False
                first_say_good_lunch = False
                first_say_good_dinner = False
                first_say_good_dream = True
                print("提醒女友晚上睡觉:%s" % time.ctime())

        # 延时10秒
        time.sleep(10)



if __name__ == "__main__":

    # 启动微信机器人，自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    if('Windows' in platform.system()):
        # Windows
        bot = Bot()
    elif('Darwin' in platform.system()):
        # MacOSX
        bot = Bot()
    elif('Linux' in platform.system()):
        # Linux
        bot = Bot(console_qr=2,cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")



    # 设置你的微信名称和对方的微信名称，记住，不是微信ID也不是微信备注
    # 你的微型名称，记住，不是微信ID也不是微信备注
    my_wechat_name = u'你的微信名字'
    # 你女友的微信名称，记住，不是微信ID也不是微信备注
    my_lady_wechat_name = u'她的微信名字'

    # 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
    say_good_morning = "07:00"
    say_good_lunch = "11:50"
    say_good_dinner = "17:50"
    say_good_dream = "23:10"

    # 不同时间段想要发送的内容
    str_good_morning = "小宝贝~起床啦~\n\n已经7点钟啦，起来晒太阳啦！"
    str_good_lunch = "ლ(°◕‵ƹ′◕ლ)亲亲,不要太累啦，中午饭记得吃哦，劳逸结合(*^__^*) 嘻嘻……"
    str_good_dinner = "n(*≧▽≦*)n小可爱，又到了下班时间啦，一起来吃晚饭吧"
    str_good_dream = "⊙﹏⊙∥∣°猪猪，晚上23点了，时间不早了哦，记得早点休息。"


    # 开始守护女友
    start_care()


