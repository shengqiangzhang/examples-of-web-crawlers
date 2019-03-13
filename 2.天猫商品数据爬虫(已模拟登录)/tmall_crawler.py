# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from time import sleep


#定义一个taobao类
class taobao_infos:

    #对象初始化
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10) #超时时长为10s


    #延时操作,并可选择是否弹出窗口提示
    def sleep_and_alert(self,sec,message,is_alert):

        for second in range(sec):
            if(is_alert):
                alert = "alert(\"" + message + ":" + str(sec - second) + "秒\")"
                self.browser.execute_script(alert)
                al = self.browser.switch_to.alert
                sleep(1)
                al.accept()
            else:
                sleep(1)


    #登录淘宝
    def login(self):

        # 打开网页
        self.browser.get(self.url)

        # 自适应等待，点击密码登录选项
        self.browser.implicitly_wait(30) #智能等待，直到网页加载完毕，最长等待时间为30s
        self.browser.find_element_by_xpath('//*[@class="forget-pwd J_Quick2Static"]').click()

        # 自适应等待，点击微博登录宣传
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="weibo-login"]').click()

        # 自适应等待，输入微博账号
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('username').send_keys(weibo_username)

        # 自适应等待，输入微博密码
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('password').send_keys(weibo_password)

        # 自适应等待，点击确认登录按钮
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()

        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)




    # 获取天猫商品总共的页数
    def search_toal_page(self):

        # 等待本页面全部天猫商品数据加载完毕
        good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList > div.product > div.product-iWrap')))

        #获取天猫商品总共页数
        number_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form')))
        page_total = number_total.text.replace("共","").replace("页，到第页 确定","").replace("，","")

        return page_total


    # 翻页操作
    def next_page(self, page_number):
        # 等待该页面input输入框加载完毕
        input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > input.ui-page-skipTo')))

        # 等待该页面的确定按钮加载完毕
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > button.ui-btn-s')))

        # 清除里面的数字
        input.clear()

        # 重新输入数字
        input.send_keys(page_number)

        # 强制延迟1秒，防止被识别成机器人
        sleep(1)

        # 点击确定按钮
        submit.click()


    # 模拟向下滑动浏览
    def swipe_down(self,second):
        for i in range(int(second/0.1)):
            js = "var q=document.documentElement.scrollTop=" + str(300+200*i)
            self.browser.execute_script(js)
            sleep(0.1)
        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.2)


    # 爬取天猫商品数据
    def crawl_good_data(self):

        # 对天猫商品数据进行爬虫
        self.browser.get("https://list.tmall.com/search_product.htm?q=羽毛球")

        # 获取天猫商品总共的页数
        page_total = self.search_toal_page()
        print("总共页数" + page_total)

        # 遍历所有页数
        for page in range(2,int(page_total)):

            # 等待该页面全部商品数据加载完毕
            good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList > div.product > div.product-iWrap')))

            # 等待该页面input输入框加载完毕
            input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > input.ui-page-skipTo')))

            # 获取当前页
            now_page = input.get_attribute('value')
            print("当前页数" + now_page + ",总共页数" + page_total)

            # 获取本页面源代码
            html = self.browser.page_source

            # pq模块解析网页源代码
            doc = pq(html)

            # 存储天猫商品数据
            good_items = doc('#J_ItemList .product').items()

            # 遍历该页的所有商品
            for item in good_items:
                good_title = item.find('.productTitle').text().replace('\n',"").replace('\r',"")
                good_status = item.find('.productStatus').text().replace(" ","").replace("笔","").replace('\n',"").replace('\r',"")
                good_price = item.find('.productPrice').text().replace("¥", "").replace(" ", "").replace('\n', "").replace('\r', "")
                good_url = item.find('.productImg').attr('href')
                print(good_title + "   " + good_status + "   " + good_price + "   " + good_url + '\n')


            # 精髓之处，大部分人被检测为机器人就是因为进一步模拟人工操作
            # 模拟人工向下浏览商品，即进行模拟下滑操作，防止被识别出是机器人
            self.swipe_down(2)

            # 翻页，下一页
            self.next_page(page)

            # 等待滑动验证码出现,超时时间为5秒，每0.5秒检查一次
            # 大部分情况不会出现滑动验证码，所以如果有需要可以注释掉下面的代码
            # sleep(5)
            WebDriverWait(self.browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, "nc_1_n1z"))) #等待滑动拖动控件出现
            try:
                swipe_button = self.browser.find_element_by_id('nc_1_n1z') #获取滑动拖动控件

                #模拟拽托
                action = ActionChains(self.browser) # 实例化一个action对象
                action.click_and_hold(swipe_button).perform() # perform()用来执行ActionChains中存储的行为
                action.reset_actions()
                action.move_by_offset(580, 0).perform() # 移动滑块

            except Exception as e:
                print ('get button failed: ', e)


if __name__ == "__main__":

    # 使用之前请先查看当前目录下的使用说明文件README.MD
    # 使用之前请先查看当前目录下的使用说明文件README.MD
    # 使用之前请先查看当前目录下的使用说明文件README.MD

    chromedriver_path = "/Users/bird/Desktop/chromedriver.exe" #改成你的chromedriver的完整路径地址
    weibo_username = "改成你的微博账号" #改成你的微博账号
    weibo_password = "改成你的微博密码" #改成你的微博密码

    a = taobao_infos()
    a.login() #登录
    a.crawl_good_data() #爬取天猫商品数据