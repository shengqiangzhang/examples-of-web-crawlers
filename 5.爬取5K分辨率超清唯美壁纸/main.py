# -*- coding:utf-8 -*-

import requests
from filetype import guess
from os import rename
from os import makedirs
from os.path import exists
import json
from contextlib import closing

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

def get_photo_type():
    """
    获取可以爬取的壁纸类型
    :return:
    """
    url = "https://service.paper.meiyuan.in/api/v2/columns"
    res = requests.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    return res_json



def down_load(file_url, file_full_name, now_photo_count, all_photo_count):
    """
    文件下载器
    :param file_url:
    :param file_full_name:
    :param now_photo_count:
    :param all_photo_count:
    :return:
    """

    # 开始下载图片
    with closing(requests.get(file_url, headers=headers, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 文件总大小
        data_count = 0  # 当前已传输的大小
        with open(file_full_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                done_block = int((data_count / content_size) * 50)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r %s：[%s%s] %d%% %d/%d" % (file_full_name, done_block * '█', ' ' * (50 - 1 - done_block), now_jd, now_photo_count, all_photo_count), end=" ")

    # 下载完图片后获取图片扩展名，并为其增加扩展名
    file_type = guess(file_full_name)
    rename(file_full_name, file_full_name + '.' + file_type.extension)

def crawler_photo(type_id, photo_count):
    """
    爬取不同类型图片
    :param type_id:
    :param photo_count:
    :return:
    """

    url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/{}?page=1&per_page={}'.format(type_id, photo_count)

    # 获取图片列表数据
    respond = requests.get(url, headers=headers, verify=False)
    photo_data = json.loads(respond.content)

    # 已经下载的图片张数
    now_photo_count = 1

    # 所有图片张数
    all_photo_count = len(photo_data)

    # 开始下载并保存5K分辨率壁纸
    for photo in photo_data:

        # 创建一个文件夹存放下载的图片
        if not exists('./' + str(type_id)):
            makedirs('./' + str(type_id))

        # 准备下载的图片链接
        file_url = photo['urls']['raw']

        # 准备下载的图片名称,不包含扩展名
        file_name_only = file_url.split('/')
        file_name_only = file_name_only[len(file_name_only) - 1]

        # 准备保存到本地的完整路径
        file_full_name = './' + str(type_id) + '/' + file_name_only

        # 开始下载图片
        down_load(file_url, file_full_name, now_photo_count, all_photo_count)
        now_photo_count = now_photo_count + 1



if __name__ == '__main__':

    # 获取可以爬取的壁纸类型
    res_json = get_photo_type()

    # 壁纸类型
    wall_paper_id = 0

    # 壁纸数量
    wall_paper_count = 10

    info_str = "壁纸类型："
    for index, p_type in enumerate(res_json):
        info_str = info_str + "{} {}".format(index, p_type['langs']['zh-Hans-CN'])
        if index != len(res_json) - 1:
            info_str = info_str + ", "

    # 选择壁纸类型，并判断输入是否正确
    while True:
        wall_paper_id = input(info_str + "\n请输入编号以便选择5K超清壁纸类型：")
        wall_paper_id = wall_paper_id.strip()
        wall_paper_id = int(wall_paper_id)
        if wall_paper_id >= len(res_json) or wall_paper_id < 0:
            continue
        else:
            break

    # 选择壁纸数量，并判断输入是否正确
    while True:
        wall_paper_count = input("请输入要下载的5K超清壁纸的数量：")
        wall_paper_count = wall_paper_count.strip()
        wall_paper_count = int(wall_paper_count)
        if wall_paper_count <= 0:
            continue
        else:
            break

    # 开始爬取5K高清壁纸
    print("正在下载5K超清壁纸，请稍等……")
    crawler_photo(res_json[wall_paper_id]['_id'], wall_paper_count)
    print('\n下载5K高清壁纸完毕，壁纸位于当前的{}目录。'.format(res_json[wall_paper_id]['_id']))



