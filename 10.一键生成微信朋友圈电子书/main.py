# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from os.path import exists
from os import makedirs
from os import listdir
from shutil import rmtree
import time
from PIL import Image

# 初始化所需文件夹
def init_folders():

    for dir in ['img_data']:
        if(not exists(dir)):
            # 目录不存在时则创建
            makedirs(dir)
        else:
            # 目录存在时则先删除递归删除该目录再重新创建
            rmtree(dir)
            makedirs(dir)


# 拼接所有图片成一张长图
def merge_picture():

    # 获取img_dat目录下所有Png图像
    ims = [Image.open('img_data/' + fn) for fn in listdir('img_data') if fn.endswith('.png')]

    # 获取单张图片的尺寸
    width, height = ims[0].size

    # 创建一个空白的长图
    result = Image.new(ims[0].mode, (width, height * len(ims)))

    # 拼接图片
    for i, im in enumerate(ims):
        print(u'({}/{})正在拼接朋友圈数据中，请耐心等待……'.format(i+1, len(ims)))
        result.paste(im, box=(0, i * height))

    # 保存长图
    print(u'拼接完成，正在保存到本地文件中，请耐心等待……')
    result.save('朋友圈数据.png')
    print(u'保存成功，文件名为[朋友圈数据.png]，存放于当前目录下')



if __name__ == '__main__':

    # chromedriver驱动文件的位置，可输入绝对路径或者相对路径，./表示当前目录下
    # './chromedriver_win32.exe'表示当前目录下的chromedriver_win32.exe文件
    # 不同系统和不同chrome版本需要下载不同的chromedriver，请下载合适自己的版本
    # 下载地址http://chromedriver.chromium.org/downloads
    chromedriver_path = './chromedriver_mac64_74'

    # 你的微信朋友圈数据地址，注意不要泄露给其他人
    target_url = 'https://chushu.la/book/chushula-918509291'






    # 初始化相关目录
    init_folders()

    # 屏蔽chrome的提示
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')

    # 绑定Chrome和chromedriver，不同Chrome版本对应的chromedriver是不同的，请注意
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=option)

    # 将浏览器最大化显示，使得截图效果更好
    driver.maximize_window()
    # 延迟2秒，给最大化过程一点时间
    time.sleep(2)

    # 模拟浏览指定网页
    driver.get(target_url)


    # 开始无限翻页，直到最后翻到一页
    for i in range(0, 10000):

        # 等待 下一月控件 出现
        next_month = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.next-month')))

        # 等待 下一月控件 可见才能模拟点击，不可见的元素点击了会出错
        while(True):
            if(next_month.is_displayed() == True):
                break


        # 隐藏导航栏，防止影响截图效果
        js = 'document.querySelector("body > header").style.display="none";'
        driver.execute_script(js)


        # 等待所有数据加载完毕，正常情况下数据加载完毕后，这个‘加载中’元素会隐藏起来
        while(True):
            loading_status = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.j-save-popup.save-popup')))
            if(loading_status.is_displayed() == False):
                break



        # 由于网站的图片是懒加载形式，所以需要挨个定位到每张图片的位置使该图片加载成功
        # 每次寻找类名为lazy-img的img元素集合，当元素集合至少存在一个元素，则定位到第一个元素
        # 当元素集合不存在任何元素，则说明懒加载的图片已经没有了，可以退出循环了
        while (True):
            try:
                lazy_img = driver.find_elements_by_css_selector('img.lazy-img')
                js = 'document.getElementsByClassName("lazy-img")[0].scrollIntoView();'
                driver.execute_script(js)
                time.sleep(0.2)
            except:
                # 找不到控件img.lazy-img，所以退出循环
                break


        # 等待 主页面控件 出现。这里主页面控件绝大部分情况下是早就加载完毕了，但是为了保险起见，多增加这层等待
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.main')))
        main = driver.find_element_by_css_selector('ul.main')
        element_left_list = main.find_elements_by_css_selector('div.con-left')
        element_right_list = main.find_elements_by_css_selector('div.con-right')


        # 稍微延迟下，给懒加载的图片完全显示提供一点时间
        time.sleep(2)


        # 开始截图朋友圈数据元素，分为左右页
        for index, element in enumerate(element_left_list):
            if(element.is_displayed() == True):
                element.screenshot('img_data/' + '{}-{}-0.png'.format(i, index))

        for index, element in enumerate(element_right_list):
            if(element.is_displayed() == True):
                element.screenshot('img_data/' + '{}-{}-1.png'.format(i, index))


        # 判断当下一月控件的class name 是否为next-month disable，如果是，则说明翻到最后一页了，可以跳出循环了，否则模拟点击下一月控件
        page_source=driver.page_source
        if('next-month disable' in page_source):
            break


        # 截图完这一月的数据后，模拟点击 下一月控件
        next_month.click()
        # 稍微延时
        time.sleep(1)



    # 提示
    print(u'翻页完毕')

    # 延时1秒
    time.sleep(1)

    # 拼接所有图片成一张长图
    merge_picture()

    # 提示
    print(u'拼接完毕')

    # 关闭浏览器
    driver.quit()
