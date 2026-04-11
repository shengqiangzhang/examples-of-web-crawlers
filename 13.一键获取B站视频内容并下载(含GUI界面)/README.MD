# B站视频获取下载

本项目是一个基于 Python 开发的图形界面程序，用于从 Bilibili 视频页面提取音视频流并进行下载与合并。适用于支持 DASH 流的视频内容。

---

## 项目功能

- 输入 Bilibili 视频链接即可下载
- 自动提取视频的音频和视频流
- 自动获取视频标题并清洗为有效文件名
- 图形化界面操作，进度实时更新
- 使用 `ffmpeg` 合并音视频为 MP4 文件
- 支持中文、特殊字符、空格、Emoji 等命名

---

## 环境要求

- Python 3.7 及以上版本
- 系统平台：Windows（建议）
- 已配置 ffmpeg 可执行文件路径（本项目附带）

---

## 安装依赖

项目仅依赖一个外部库：`requests`。

请使用如下命令安装：

```bash
pip install requests
```

请自行将.\ffmpeg\bin 添加至系统变量中的Path中。

---

## 如何运行

只需要按照以下命令即可运行：

```bash
# 跳转到当前目录
cd 目录名
# 开始运行
python getVideo.py

# 运行成功后，通过GUI操作即可
如果需要使用cookie，在输入框输入以下内容，每一项都可以在F12内找到，替换为自己的：
SESSDATA=; bili_jct=; DedeUserID=; DedeUserID__ckMd5=;
```