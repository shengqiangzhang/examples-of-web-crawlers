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
    time.sleep(2)
    driver.get('https://chushu.la/book/chushula-918509291')
    driver.implicitly_wait(60)
    print(u'页面加载完毕')






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

        # 判断当下一月控件的class name 是否为next-month disable，如果是，则说明翻到最后一页了
        page_source=driver.page_source
        if('next-month disable' in page_source):

            # 等待 主页面控件 出现。大部分情况下，经常上面的滚动操作，主页面控件都是已经出现了的。
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


            # 获取页面高度，以便知道要滑动多少次才能到底部
            time.sleep(3)
            html = driver.find_element_by_css_selector('html')
            html_height = (html.size)['height']
            print(html.size)


            # 模拟人工向下滑动，使得图片能够加载
            # 经过查看源代码分析得知，每一小页的高度为780px
            for j in range(0, 999):
                position = 780 * (j+1)
                js = "var q=document.documentElement.scrollTop=" + str(position)
                driver.execute_script(js)
                time.sleep(3)

                if(position > html_height):
                    break


            # 开始截取元素
            element_left_list = main.find_elements_by_css_selector('div.con-left')
            element_right_list = main.find_elements_by_css_selector('div.con-right')
            for index, element in enumerate(element_left_list):
                if(element.is_displayed() == True):
                    element.screenshot('{}-{}-left.png'.format(i, index))

            for index, element in enumerate(element_right_list):
                if(element.is_displayed() == True):
                    element.screenshot('{}-{}-right.png'.format(i, index))

            break


    print(u'翻页完毕')
    js = 'alert("下载完毕")'
    driver.execute_script(js)


    #关闭浏览器
    # driver.quit()
