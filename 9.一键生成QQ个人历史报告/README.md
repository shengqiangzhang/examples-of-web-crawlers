# 9.一键生成QQ个人历史报告


## 简介

近几年，由于微信的流行，大部分人不再频繁使用QQ，所以我们对于自己的QQ数据并不是特别了解。我相信，如果能够生成一份属于自己的QQ历史报告，那将是无比开心的一件事。



目前网上关于QQ的数据分析工具较少，原因是QQ相关接口比较复杂。**而本程序的运行十分简单，具有良好的用户交互界面，只需要扫码登录一步操作即可。**



目前本程序获取的数据包括：QQ详细数据、手机在线时间、非隐身状态下在线时间、QQ活跃时间、单向好友数量、QQ财产分析、群聊分析、过去一年我退出的群聊数据、退去一个月我删除的好友数据、所有代付信息、我最在意的人以及最在意我的人。**由于相关的数据接口有访问限制，所以本程序并没有对QQ好友进行分析。**



## 功能截图

![](example1.png)
![](example2.png)
![](example3.png)
![](example4.png)


## 如何运行
```bash
# 跳转到当前目录
cd 目录名
# 先卸载依赖库
pip uninstall -y -r requirement.txt
# 再重新安装依赖库
pip install -r requirement.txt
# 开始运行
python main.py
```



## 编写思路

1. 本程序分为多个模块


## 补充

完整版源代码存放在[github][5]上，有需要的可以下载

项目持续更新，欢迎您[star本项目][5]

## License
[The MIT License (MIT)][6]

[5]:https://github.com/shengqiangzhang/examples-of-web-crawlers
[6]:http://opensource.org/licenses/MIT