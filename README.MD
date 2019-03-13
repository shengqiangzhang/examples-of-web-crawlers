# 简介
一些常见的网站爬虫例子，代码通用性较高，时效性较久。**项目代码对新手比较友好**，尽量用简单的python代码，并配有大量注释。

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