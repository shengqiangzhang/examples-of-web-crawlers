# -*- coding:utf-8 -*-

import os
import PIL.Image as Image
from os import listdir
import math
from tqdm import tqdm







if __name__ == '__main__':

    # 拼接头像
    pics = listdir('image')  # 得到user目录下的所有文件，即各个好友头像
    numPic = len(pics)
    eachsize = int(math.sqrt(float(640 * 640) / numPic))  # 先圈定每个正方形小头像的边长，如果嫌小可以加大
    numrow = int(640 / eachsize)
    numcol = int(numPic / numrow)  # 向下取整
    toImage = Image.new('RGB', (eachsize * numrow, eachsize * numcol))  # 先生成头像集模板

    x = 0  # 小头像拼接时的左上角横坐标
    y = 0  # 小头像拼接时的左上角纵坐标

    for i in tqdm(pics):
        try:
            # 打开图片
            img = Image.open('image/' + i)
        except IOError:
            print("Error: 没有找到文件或读取文件失败")
        else:
            # 缩小图片
            img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
            # 拼接图片
            toImage.paste(img, (x * eachsize, y * eachsize))
            x += 1
            if x == numrow:
                x = 0
                y += 1

    toImage.save('data/拼接' + ".jpg")


    # 生成一个网页
    with open('data/微信好友头像拼接图.html', 'w', encoding='utf-8') as f:
        data = '''
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                  <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
                  <meta charset="utf-8" /> 
                  <title>微信好友头像拼接图</title> 
            </head>
            <body>
                <p><font size=4px><strong>微信好友头像拼接图</strong></font></p>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <img src="拼接.jpg" />
            </body>
            </html>
        '''
        f.write(data)