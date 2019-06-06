# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


if __name__ == '__main__':
    # http://chromedriver.chromium.org/downloads
    driver = webdriver.Chrome(executable_path='./chromedriver_mac64_74')
    # 将浏览器最大化显示
    driver.maximize_window()
    time.sleep(1)

    # 跳转到指定网址
    driver.get('https://chushu.la/book/chushula-918509291')


    for i in range(0, 10000):

        # 等待 下一月控件 出现
        next_month = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.next-month')))

        # 等待 下一月控件 可见才能模拟点击
        while(True):
            if(next_month.is_displayed() == True):
                break


        # 隐藏导航栏，防止影响截图效果
        js = 'document.querySelector("body > header").style.display="none";'
        driver.execute_script(js)


        # 模拟点击 下一月控件
        next_month.click()

        # 延时
        time.sleep(1)

        # 判断当下一月控件的class name 是否为next-month disable，如果是，则说明翻到最后一月了
        page_source = driver.page_source
        if('next-month disable' in page_source):

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


            # 由于网站的图片是懒加载形式，所以需要挨个定位到每张图片的位置
            # 每次寻找是否存在类名为lazy-img的img元素集合，当元素集合至少存在一个元素，则定位到第一个元素
            # 当元素集合不存在任何元素，则说明懒加载的图片已经没有了，可以退出循环了
            while(True):
                try:
                    lazy_img = driver.find_elements_by_css_selector('img.lazy-img')
                    js = 'document.getElementsByClassName("lazy-img")[0].scrollIntoView();'
                    driver.execute_script(js)
                    time.sleep(0.2)
                except:
                    # 找不到控件img.lazy-img，所以退出循环
                    break




            # 开始截取元素
            element_left_list = main.find_elements_by_css_selector('div.con-left')
            element_right_list = main.find_elements_by_css_selector('div.con-right')
            for index, element in enumerate(element_left_list):
                if(element.is_displayed() == True):
                    print(element.get_attribute('class'))
                    # element.screenshot('{}-{}-0.png'.format(i, index))
                    # time.sleep(1)

            for index, element in enumerate(element_right_list):
                if(element.is_displayed() == True):
                    print(element.get_attribute('class'))
                    # element.screenshot('{}-{}-1.png'.format(i, index))
                    # time.sleep(1)

            break


    print(u'翻页完毕')


    #关闭浏览器
    # driver.quit()
