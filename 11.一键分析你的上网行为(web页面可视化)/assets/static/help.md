## 如何获取chrome历史记录文件?

### Windows Vista, Windows 7,  Windows 8, Windows 10
- 历史记录文件位置: `C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\History`

- 拷贝历史记录文件到桌面: 
```bash
# 打开命令行cmd,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
copy "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\History" "C:\Users\%USERNAME%\Desktop\History"
```

- **注意说明**: `%USERNAME%`为你的用户名, 如果执行命令出现错误, 请手动找到该历史记录文件。

<br />

### Windows XP

- 历史记录文件位置: `C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\Default\History`

- 拷贝历史记录文件到桌面: 
```bash
# 打开命令行cmd,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
copy "C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\Default\History" "C:\Documents and Settings\%USERNAME%\Desktop\History"
```

- **注意说明**: `%USERNAME%`为你的用户名, 如果执行命令出现错误, 请手动找到该历史记录文件。

<br />

### Mac OS X

- 历史记录文件位置: `~/Library/Application Support/Google/Chrome/Default/History`

- 拷贝历史记录文件到桌面:
```bash
# 打开terminal,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
cp ~/Library/Application\ Support/Google/Chrome/Default/History ~/Desktop/History
```

- **注意说明**: `Application Support`中的空格需要转义，所以改为`Application\ Support`

<br />

### Linux/ Unix
- 历史记录文件位置:  `~/.config/google-chrome/Default/History`

- 拷贝历史记录文件到桌面: 
```bash
# 打开terminal,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
cp ~/.config/google-chrome/Default/History ~/Desktop/History
```

- **注意说明**: `如果提示路径不存在, 请自行获取History文件`

<br />
<br />
<br />
<br />
<br />

## 是否存在窃取隐私问题?

**不存在。本项目为开源项目。**

**如果你担心出现窃取隐私的情况**, 请[点击跳转到GitHub](https://github.com/shengqiangzhang/examples-of-web-crawlers/tree/master/11.%E4%B8%80%E9%94%AE%E5%88%86%E6%9E%90%E4%BD%A0%E7%9A%84%E4%B8%8A%E7%BD%91%E8%A1%8C%E4%B8%BA(web%E9%A1%B5%E9%9D%A2%E5%8F%AF%E8%A7%86%E5%8C%96))下载源代码运行。