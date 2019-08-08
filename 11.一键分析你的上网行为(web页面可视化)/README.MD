## Windows Vista, Windows 7,  Windows 8, Windows 10
- 历史记录文件位置: `C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\History`

- 拷贝历史记录文件到桌面: 
```bash
# 打开命令行cmd,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
copy "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\History" "C:\Users\%USERNAME%\Desktop\History"
```

- **注意说明**: `%USERNAME%`为你的用户名, 如果执行命令出现错误, 请手动找到该历史记录文件。

<br />

## Windows XP

- 历史记录文件位置: `C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\Default\History`

- 拷贝历史记录文件到桌面: 
```bash
# 打开命令行cmd,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
copy "C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\Default\History" "C:\Documents and Settings\%USERNAME%\Desktop\History"
```

- **注意说明**: `%USERNAME%`为你的用户名, 如果执行命令出现错误, 请手动找到该历史记录文件。

<br />

## Mac OS X

- 历史记录文件位置: `~/Library/Application Support/Google/Chrome/Default/History`

- 拷贝历史记录文件到桌面:
```bash
# 打开terminal,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
cp ~/Library/Application\ Support/Google/Chrome/Default/History ~/Desktop/History
```

- **注意说明**: `Application Support`中的空格需要转义，所以改为`Application\ Support`

<br />

## Linux/ Unix
- 历史记录文件位置:  `~/.config/google-chrome/Default/History`

- 拷贝历史记录文件到桌面: 
```bash
# 打开terminal,输入以下命令, 自动将History文件复制到桌面, 文件名为History, 没有后缀名
cp ~/.config/google-chrome/Default/History ~/Desktop/History
```

- **注意说明**: `如果提示路径不存在, 请自行获取History文件`