# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from platform import system
import time
import json
import os
import random

# 引入打开文件所用的库
# Window与Linux和Mac OSX有所不同
# lambda用来定义一个匿名函数，可实现类似c语言的define定义
if('Windows' in system()):
    # Windows
    from os import startfile
    open_pdf_file = lambda x : startfile(x)
elif('Darwin' in system()):
    # MacOSX
    from subprocess import call
    open_pdf_file = lambda x : call(["open", x])
else:
    # Linux
    from subprocess import call
    open_pdf_file = lambda x: call(["xdg-open", x])


# 以网页输入文本框形式提示用户输入url地址
def input_url():

    while(True):

        # js脚本
        random_id = [str(random.randint(0, 9)) for i in range(0,10)]
        random_id = "".join(random_id)
        random_id = 'id_input_target_url_' + random_id
        js = """
            // 弹出文本输入框，输入微信书的完整链接地址
            target_url = prompt("请输入微信书的完整链接地址","https://");
            
            // 动态创建一个input元素
            input_target_url = document.createElement("input");
            // 为其设置id，以便在程序中能够获取到它的值
            input_target_url.id = "id_input_target_url";
            
            // 插入到当前网页中
            document.getElementsByTagName("body")[0].appendChild(input_target_url);
            
            // 设置不可见
            document.getElementById("id_input_target_url").style.display = 'none';
            
            // 设置value为target_url的值
            document.getElementById("id_input_target_url").value = target_url
        """
        js = js.replace('id_input_target_url', random_id)


        # 执行以上js脚本
        driver.execute_script(js)

        # 判断弹出框是否存在
        while(True):
            try:
                # 检测是否存在弹出框
                alert = driver.switch_to.alert
                time.sleep(0.5)
            except:
                # 如果抛异常，说明当前页面不存在弹出框，即用户点击了取消或者确定
                break


        # 获取用户输入的链接地址
        target_url = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, random_id)))
        value = target_url.get_attribute('value')
        # 删除空格
        value = value.strip()


        # 判断输入的链接地址是否正确
        if( value != '' and 'https://chushu.la' in value):
            break


    return value




if __name__ == '__main__':


    # chromedriver驱动文件的位置，可输入绝对路径或者相对路径，./表示当前目录下
    # './chromedriver_win32.exe'表示当前目录下的chromedriver_win32.exe文件
    # 不同系统和不同chrome版本需要下载不同的chromedriver，请下载合适自己的版本
    # chromedriver下载地址http://chromedriver.chromium.org/downloads
    # 默认的chromedriver支持的Chrome版本为74
    # chromedriver_path = './chromedriver_win32_74.0.3729.6.exe'
    chromedriver_path = './chromedriver_mac_74.0.3729.6'




    option = webdriver.ChromeOptions()
    # 屏蔽chrome的提示
    option.add_argument('disable-infobars')
    # 静默自动打印为高清PDF文件，并存储到os.getcwd()目录，也就是当前目录
    appState = {
        # 添加保存为pdf选项
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                 "account":""
            }
        ],
        # 选择保存为pdf选项
        "selectedDestinationId": "Save as PDF",
        # 版本2
        "version": 2,
        # 不显示页眉页脚
        "isHeaderFooterEnabled": False
    }

    profile = {
        # 打印前置参数
        'printing.print_preview_sticky_settings.appState': json.dumps(appState),
        # 默认下载、打印保存路径
        'savefile.default_directory': os.getcwd()
    }

    # 添加实验性质的设置参数
    option.add_experimental_option('prefs', profile)

    # 添加启动参数，后台静默打印
    option.add_argument('--kiosk-printing')


    # 绑定Chrome和chromedriver，不同Chrome版本对应的chromedriver是不同的，请注意
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=option)

    # 将浏览器最大化显示，使得截图效果更好
    driver.maximize_window()

    # 延迟2秒，给最大化过程一点时间
    time.sleep(2)



    # 你的微信朋友圈数据地址，注意不要泄露给其他人
    # 在调试过程中，可以直接给target_url赋值
    target_url = input_url()

    # 模拟浏览指定网页
    driver.get(target_url)

    for i in range(0, 10000):

        # 等待当前页面所有数据加载完毕，正常情况下数据加载完毕后，这个‘加载中’元素会隐藏起来
        while (True):
            loading_status = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.j-save-popup.save-popup')))
            if (loading_status.is_displayed() == False):
                break

        # 隐藏导航栏，防止影响截图效果
        js = 'document.querySelector("body > header").style.display="none";'
        driver.execute_script(js)

        # 等待 下一月控件 出现
        next_month = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.next-month')))

        # 等待 下一月控件 可见才能模拟点击
        while(True):
            if(next_month.is_displayed() == True):
                break

        # 模拟点击 下一月控件
        time.sleep(0.5)
        next_month.click()


        # 判断当下一月控件的class name 是否为next-month disable，如果是，则说明翻到最后一月了
        page_source = driver.page_source
        if('next-month disable' in page_source):

            # 等待当前页面所有数据加载完毕，正常情况下数据加载完毕后，这个‘加载中’元素会隐藏起来
            while (True):
                loading_status = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.j-save-popup.save-popup')))
                if (loading_status.is_displayed() == False):
                    break


            # 等待 主页面控件 出现
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.main')))
            main = driver.find_element_by_css_selector('ul.main')
            element_left_list = main.find_elements_by_css_selector('div.con-left')


            # 每一个element代表每一页，将每一页中style的display属性改成block，即可见状态
            for index, element in enumerate(element_left_list):
                # ..在xpath中表示上一级的元素，也就是父元素
                parent_element = element.find_element_by_xpath('..')
                # 获取这个父元素的完整id
                parent_element_id = parent_element.get_attribute('id')

                # 将该父元素更改为可见状态
                js = 'document.getElementById("{}").style.display="block";'.format(parent_element_id)
                driver.execute_script(js)

                # 将每一页之间的间隔去掉
                js = 'document.getElementById("{}").style.marginTop="0px";'.format(parent_element_id)
                driver.execute_script(js)



            # 由于网站的图片是懒加载形式，所以需要挨个定位到每张图片的位置
            # 每次寻找是否存在类名为lazy-img的img元素集合，当元素集合至少存在一个元素，则定位到第一个元素
            # 当元素集合不存在任何元素，则说明懒加载的图片已经没有了，可以退出循环了
            while(True):
                try:
                    lazy_img = driver.find_elements_by_css_selector('img.lazy-img')
                    js = 'document.getElementsByClassName("lazy-img")[0].scrollIntoView();'
                    driver.execute_script(js)
                    time.sleep(3)
                except:
                    # 找不到控件img.lazy-img，所以退出循环
                    break


            break




    # 调用chrome打印功能
    driver.execute_script('window.print();')


    # 调用系统方式自动打开这个pdf文件
    pdf_file_name = '{}.pdf'.format(driver.title)
    print(u'生成完毕，已为你自动打开 {}'.format(pdf_file_name))
    open_pdf_file(pdf_file_name)

    # 退出浏览器
    driver.quit()
