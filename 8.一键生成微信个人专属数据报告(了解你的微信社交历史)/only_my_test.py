from pyecharts import Pie
from pyecharts import Map
import subprocess
from wxpy import *
from platform import system
import os
import subprocess
import shutil
from tqdm import tqdm
from pyecharts import Pie
from pyecharts import Map

if(__name__ == '__main__'):

    # 使用一个字典统计好友地区分布数量
    province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
                     '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
                     '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
                     '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
                     '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
                     '四川': 0, '贵州': 0, '云南': 0,
                     '内蒙古': 0, '新疆': 0, '宁夏': 0, '广西': 0, '西藏': 0,
                     '香港': 0, '澳门': 0}
    # provice = list(province_dict.keys())
    # values = list(province_dict.values())
    #
    #
    # # maptype='china' 只显示全国直辖市和省级，数据只能是省名和直辖市的名称
    # map = Map("微信好友地区分布")
    # map.add("", provice, values, visual_range=[0, 50], maptype='china', is_visualmap=True, visual_text_color='#000')
    # map.render(path="./data/sex_ratio2.html")

    # 调用系统方式打开这个html文件
    if('Windows' in system()):
        # Windows
        os.startfile('./微信个人数据报告.html')
    elif('Darwin' in system()):
        # MacOSX
        subprocess.call(["open", './微信个人数据报告.html'])
    elif('Linux' in system()):
        # Linux
        subprocess.call(["xdg-open", './微信个人数据报告.html'])
    else:
        # 自行确定
        print("打开微信个人数据报告文件失败，请手动打开")
        exit()



