windows平台打包成可执行exe文件

```python
# 安装pyinstaller
pip install pyinstaller

# 跳转到当前目录
cd 目录名

# 先卸载依赖库
pip uninstall -y -r requirement.txt

# 再重新安装依赖库
pip install -r requirement.txt

# 更新 setuptools
pip install --upgrade setuptools

# 开始打包
pyinstaller generate_wx_data.py
```

