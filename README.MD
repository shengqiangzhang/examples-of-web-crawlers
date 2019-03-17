# 简介
一些常见的网站爬虫例子，代码通用性较高，时效性较久。**项目代码对新手比较友好**，尽量用简单的python代码，并配有大量注释。



# 编写环境

| system         | macOS Sierra 10.12.6 |
| -------------- | -------------------- |
| python Version | Python 3.7.0         |
| Python IDE     | PyCharm              |




# 1.淘宝模拟登录
## 使用教程
1. [点击这里下载][1]下载chrome浏览器
2. 查看chrome浏览器的版本号，[点击这里下载][2]对应版本号的chromedriver驱动
3. pip安装下列包
    - [x] pip install selenium
4. [点击这里][3]登录微博，并通过微博绑定淘宝账号密码
5. 在main中填写chromedriver的绝对路径
6. 在main中填写微博账号密码

```python
#改成你的chromedriver的完整路径地址
chromedriver_path = "/Users/bird/Desktop/chromedriver.exe" 
#改成你的微博账号
weibo_username = "改成你的微博账号"
#改成你的微博密码
weibo_password = "改成你的微博密码"
```

## 演示图片
![](1.淘宝模拟登录/example.gif)  
[图片查看不了点击这里][4]

  





# 2.天猫商品数据爬虫
## 使用教程
1. [点击这里下载][1]下载chrome浏览器
2. 查看chrome浏览器的版本号，[点击这里下载][2]对应版本号的chromedriver驱动
3. pip安装下列包
    - [x] pip install selenium
    - [x] pip install pyquery
4. [点击这里][3]登录微博，并通过微博绑定淘宝账号密码
5. 在main中填写chromedriver的绝对路径
6. 在main中填写微博账号密码

```python
#改成你的chromedriver的完整路径地址
chromedriver_path = "/Users/bird/Desktop/chromedriver.exe" 
#改成你的微博账号
weibo_username = "改成你的微博账号"
#改成你的微博密码
weibo_password = "改成你的微博密码"
```

## 演示图片
![](2.天猫商品数据爬虫(已模拟登录)/example.gif)
![](2.天猫商品数据爬虫(已模拟登录)/example2.png)
[图片查看不了点击这里][4]












# 3.爬取淘宝我已购买的宝贝数据
## 使用教程
1. [点击这里下载][1]下载chrome浏览器
2. 查看chrome浏览器的版本号，[点击这里下载][2]对应版本号的chromedriver驱动
3. pip安装下列包
    - [x] pip install selenium
    - [x] pip install pyquery
4. [点击这里][3]登录微博，并通过微博绑定淘宝账号密码
5. 在main中填写chromedriver的绝对路径
6. 在main中填写微博账号密码

```python
#改成你的chromedriver的完整路径地址
chromedriver_path = "/Users/bird/Desktop/chromedriver.exe" 
#改成你的微博账号
weibo_username = "改成你的微博账号"
#改成你的微博密码
weibo_password = "改成你的微博密码"
```

## 演示图片
![](3.淘宝已买到的宝贝数据爬虫(已模拟登录)/example.gif)
![](3.淘宝已买到的宝贝数据爬虫(已模拟登录)/example2.png)
[图片查看不了点击这里][7]











# 4.每天不同时间段通过微信发消息提醒女友
## 简介

有时候，你很想关心她，但是你太忙了，以至于她一直抱怨，觉得你不够关心她。你暗自下决心，下次一定要准时发消息给她，哪怕是几句话，可是你又忘记了。你觉得自己很委屈😭，但是她又觉得你不负责。

<br />

<br />

**现在，再不用担心了**，用python就可以给女友定时发提示消息了，**而且不会漏过每一个关键时刻**，每天**早上起床、中午吃饭、晚上吃饭、晚上睡觉**，都会准时发消息给她了，而且还可以让她**学习英语单词**哦！等你了解了全部这100行代码，你可以加上每个节日自动发问候语哦，比如**三八妇女节、女神节、情人节、春节、圣诞节**，再也不用担心他说你没有仪式感了！😀

## 使用教程

- pip安装下列包
- [x] pip install wxpy
- [x] pip install requests
- 设置你的微信名字和她的微信名字

```python
    # 设置你的微信名称和对方的微信名称，记住，不是微信ID也不是微信备注
    # 你的微型名称，记住，不是微信ID也不是微信备注
    my_wechat_name = u'你的微信名字'
    # 你女友的微信名称，记住，不是微信ID也不是微信备注
    my_lady_wechat_name = u'她的微信名字'
```
- 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
```python
    # 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
    say_good_morning = "07:00"
    say_good_lunch = "11:50"
    say_good_dinner = "17:50"
    say_good_dream = "23:10"
```

- 设置想要提醒的内容
```python
    # 不同时间段想要发送的内容
    str_good_morning = "小宝贝~起床啦~\n\n已经7点钟啦，起来晒太阳啦！"
    str_good_lunch = "ლ(°◕‵ƹ′◕ლ)亲亲,不要太累啦，中午饭记得吃哦，劳逸结合(*^__^*) 嘻嘻……"
    str_good_dinner = "n(*≧▽≦*)n小可爱，又到了下班时间啦，一起来吃晚饭吧"
    str_good_dream = "⊙﹏⊙∥∣°猪猪，晚上23点了，时间不早了哦，记得早点休息。"
```

## 演示图片

![](4.每天不同时间段通过微信发消息提醒女友/example1.png)
![](4.每天不同时间段通过微信发消息提醒女友/example2.png)










# 5.爬取5K分辨率超清唯美壁纸

## 简介

壁纸的选择其实很大程度上能看出电脑主人的内心世界，有的人喜欢风景，有的人喜欢星空，有的人喜欢美女，有的人喜欢动物。然而，终究有一天你已经产生审美疲劳了，但你下定决定要换壁纸的时候，又发现网上的壁纸要么分辨率低，要么带有水印。

<br />

<br />

这里有一款Mac下的小清新壁纸神器[Pap.er][8]，可能是Mac下最好的壁纸软件，**自带5K超清分辨率壁纸**，富有多种类型壁纸，当我们想在Windows或者Linux下使用的时候，就可以考虑将**5K超清分辨率壁纸**爬取下来。

## 使用教程

1. 确保以下库均已安装：

```python
# 如果没有安装，请使用pip install module安装
import requests
import filetype
import os
import json
from contextlib import closing
```

## 演示图片

![](5.爬取5K分辨率超清唯美壁纸/example1.png)

![](5.爬取5K分辨率超清唯美壁纸/example2.gif)












# 6.爬取豆瓣排行榜电影数据(含GUI界面版)


## 简介

这个项目源于大三某课程设计。平常经常需要搜索一些电影，但是不知道哪些评分高且评价人数多的电影。为了方便使用，就将原来的项目重新改写了。当做是对爬虫技术、可视化技术的实践了。主要是通过从排行榜和从影片关键词两种方式爬取电影数据。



## 使用教程

1. 打开[http://chromedriver.storage.googleapis.com/index.html][9]，根据自己的操作系统下载对应的chromedriver
2. 打开当前面目录下的**<u>getMovieInRankingList.py</u>**，定位到第59行，将`executable_path=/Users/bird/Desktop/chromedriver.exe`修改成你自己的chromedriver路径
3. 打开pycharm，依次安装以下包
- pip install Pillow
- pip install selenium



## 演示图片

![](6.爬取豆瓣排行榜电影数据(含GUI界面版)/example_rating.png)

![](6.爬取豆瓣排行榜电影数据(含GUI界面版)/example_keyword.png)



## 包含功能

- [x] 根据关键字搜索电影
- [x] 根据排行榜(TOP250)搜索电影
- [x] 显示IMDB评分及其他基本信息
- [x] 提供多个在线视频站点，无需vip
- [x] 提供多个云盘站点搜索该视频，以便保存到云盘
- [x] 提供多个站点下载该视频
- [ ] 等待更新


## 存在问题

目前没有加入反爬虫策略，如果运行出现403 forbidden提示，则说明暂时被禁止，解决方式如下：

- 加入cookies
- 采用随机延时方式
- 采用IP代理池方式(较不稳定)









# 补充

项目持续更新，欢迎您[star本项目][5]






# License
[The MIT License (MIT)][6]



[1]:https://www.google.com/chrome/
[2]:http://chromedriver.storage.googleapis.com/index.html
[3]:https://account.weibo.com/set/bindsns/bindtaobao
[4]:https://raw.githubusercontent.com/shengqiangzhang/examples-of-web-crawlers/master/1.%E6%B7%98%E5%AE%9D%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/example.gif
[5]:https://github.com/shengqiangzhang/examples-of-web-crawlers
[6]:http://opensource.org/licenses/MIT
[7]:https://raw.githubusercontent.com/shengqiangzhang/examples-of-web-crawlers/master/3.%E6%B7%98%E5%AE%9D%E5%B7%B2%E4%B9%B0%E5%88%B0%E7%9A%84%E5%AE%9D%E8%B4%9D%E6%95%B0%E6%8D%AE%E7%88%AC%E8%99%AB(%E5%B7%B2%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95)/example.gif
[8]:http://paper.meiyuan.in/
[9]:http://chromedriver.storage.googleapis.com/index.html
