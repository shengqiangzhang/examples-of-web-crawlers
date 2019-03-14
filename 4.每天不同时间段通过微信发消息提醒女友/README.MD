# 每天不同时间段通过微信发消息提醒女友
## 简介

有时候，你很想关心她，但是你太忙了，以至于她一直抱怨，觉得你不够关心她。你暗自下决心，下次一定要准时发消息给她，哪怕是几句话，可是你又忘记了。你觉得自己很委屈😭，但是她又觉得你不负责。

<br />

<br />

**现在，再不用担心了**，用python就可以给女友定时发提示消息了，**而且不会漏过每一个关键时刻**，每天**早上起床、中午吃饭、晚上吃饭、晚上睡觉**，都会准时发消息给她了，而且还可以让她**学习英语单词**哦！等你了解了全部这100行代码，你可以加上每个节日自动发问候语哦，比如**三八妇女节、女神节、情人节、春节、圣诞节**，再也不用担心他说你没有仪式感了！😀



## 编写思路
为了方便快速开发，我们使用python中的wxpy模块完成微信的基本操作。

首先，，我们开始设置一些相关的参数，这些参数一看就懂，所以无需多言
```python
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
```

如果你愿意，可以在上面对时间的判断中，加入一些其他你想要的，比如**节日问候(情人节、圣诞节、三八妇女节等)**，这样你女友就更开心啦！后期如果有时间，我将会加上以上节日问候功能。😀



接着，开启微信机器人，为了程序的健壮性，自动判断一下操作系统，根据不同操作系统执行不同指令
```python
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
```



设置完相关参数以后，我们再来学习一下，如何每天教女友`学英语`
```python
# 获取每日励志精句
def get_message():
    r = requests.get("http://open.iciba.com/dsapi/")
    note = r.json()['note']
    content = r.json()['content']
    return note,content
```



教完女友`学英语`后，开始把我们的关心语发给他。这里涉及到wxpy模块的相关操作，很简单，看我的例子就会了。
```python
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
```


最后，就是如何每天定时发关心语给女友的问题了。首先来个while循环，365天无限关心😀
```python
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


        这下面还有很多代码，我就不列出来了

        # 延时10秒
        time.sleep(10)
```

上面的`first_say_good_morning`，`first_say_good_lunch`，`first_say_good_dinner`，`first_say_good_dream`是干什么用的呢？其实是用来做标志检测的，防止同一时间断内多次发送同样的消息给女友，发多了被拉黑怎么办😰，所以标志位是必须要的。


最后，输入`start_care()`开始守护女友模式吧~



## 使用教程

1. pip安装下列包
- [x] pip install wxpy
- [x] pip install requests
2. 设置你的微信名字和她的微信名字

```python
    # 设置你的微信名称和对方的微信名称，记住，不是微信ID也不是微信备注
    # 你的微型名称，记住，不是微信ID也不是微信备注
    my_wechat_name = u'你的微信名字'
    # 你女友的微信名称，记住，不是微信ID也不是微信备注
    my_lady_wechat_name = u'她的微信名字'
```
3. 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
```python
    # 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
    say_good_morning = "07:00"
    say_good_lunch = "11:50"
    say_good_dinner = "17:50"
    say_good_dream = "23:10"
```

4. 设置想要提醒的内容
```python
    # 不同时间段想要发送的内容
    str_good_morning = "小宝贝~起床啦~\n\n已经7点钟啦，起来晒太阳啦！"
    str_good_lunch = "ლ(°◕‵ƹ′◕ლ)亲亲,不要太累啦，中午饭记得吃哦，劳逸结合(*^__^*) 嘻嘻……"
    str_good_dinner = "n(*≧▽≦*)n小可爱，又到了下班时间啦，一起来吃晚饭吧"
    str_good_dream = "⊙﹏⊙∥∣°猪猪，晚上23点了，时间不早了哦，记得早点休息。"
```

## 演示图片

![](example1.png)
![](example2.png)


## 完整源代码
项目源代码在[GitHub仓库][5]

项目持续更新，欢迎您[star本项目][5]



# License
[The MIT License (MIT)][6]



[5]:https://github.com/shengqiangzhang/examples-of-web-crawlers
[6]:http://opensource.org/licenses/MIT
[7]:https://raw.githubusercontent.com/shengqiangzhang/examples-of-web-crawlers/master/3.%E6%B7%98%E5%AE%9D%E5%B7%B2%E4%B9%B0%E5%88%B0%E7%9A%84%E5%AE%9D%E8%B4%9D%E6%95%B0%E6%8D%AE%E7%88%AC%E8%99%AB(%E5%B7%B2%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95)/example.gif
[8]:https://raw.githubusercontent.com/shengqiangzhang/examples-of-web-crawlers/master/1.%E6%B7%98%E5%AE%9D%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/example.gif