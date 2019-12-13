# -*- coding:utf-8 -*-

from wxpy import *
from platform import system
from os.path import exists
from os import makedirs
from os import listdir
from shutil import rmtree
from queue import Queue
from threading import Thread
from time import sleep
from pyecharts.charts import Pie
from pyecharts.charts import Map
from pyecharts.charts import WordCloud
from pyecharts.charts import Bar
from pyecharts import options as opts
from requests import post
import PIL.Image as Image
import re
import random
import math
from cv2 import CascadeClassifier
from cv2 import imread
from cv2 import cvtColor
from cv2 import COLOR_BGR2GRAY


# 引入打开文件所用的库
# Window与Linux和Mac OSX有所不同
# lambda用来定义一个匿名函数，可实现类似c语言的define定义
if('Windows' in system()):
    # Windows
    from os import startfile
    open_html = lambda x : startfile(x)
elif('Darwin' in system()):
    # MacOSX
    from subprocess import call
    open_html = lambda x : call(["open", x])
else:
    # Linux
    from subprocess import call
    open_html = lambda x: call(["xdg-open", x])


# 分析好友性别比例
def sex_ratio():

    # 初始化
    male, female, other = 0, 0, 0

    # 遍历
    for user in friends:
        if(user.sex == 1):
            male += 1
        elif(user.sex == 2):
            female += 1
        else:
            other += 1

    name_list = ['男性', '女性', '未设置']
    num_list = [male, female, other]

    pie = Pie()
    pie.add("微信好友性别比例", [list(z) for z in zip(name_list, num_list)])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="微信好友性别比例"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render('data/好友性别比例.html')


# 分析好友地区分布
def region_distribution():

    # 使用一个字典统计好友地区分布数量
    province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
                     '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
                     '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
                     '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
                     '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
                     '四川': 0, '贵州': 0, '云南': 0, '内蒙古': 0, '新疆': 0,
                     '宁夏': 0, '广西': 0, '西藏': 0, '香港': 0, '澳门': 0}

    # 遍历
    for user in friends:
        # 判断省份是否存在，有可能是外国的，这种情况不考虑
        if (user.province in province_dict):
            key = user.province
            province_dict[key] += 1

    province = list(province_dict.keys())
    values = list(province_dict.values())


    # maptype='china' 只显示全国直辖市和省级，数据只能是省名和直辖市的名称
    map = Map()
    map.add("微信好友地区分布", [list(z) for z in zip(province, values)], "china")
    map.set_global_opts(
            title_opts=opts.TitleOpts(title="微信好友地区分布"),
            visualmap_opts=opts.VisualMapOpts(),
        )
    map.render(path="data/好友地区分布.html")



    # 对好友数最多的省份进行一进步分析
    max_count_province = ''
    for key, value in province_dict.items():
        if(value == max(province_dict.values())):
            max_count_province = key
            break

    # 使用一个字典统计好友地区分布数量
    city_dict = {}
    # 遍历
    for user in friends:
        if(user.province == max_count_province):
            # 更新键值对
            if(user.city in city_dict.keys()):
                city_dict[user.city] += 1
            else:
                city_dict[user.city] = 1

    bar = Bar()
    bar.add_xaxis([x for x in city_dict.keys()])
    bar.add_yaxis("地区分布", [x for x in city_dict.values()])
    bar.render('data/某省好友地区分布.html')


# 统计认识的好友的比例
def statistics_friends():
    # 初始化
    unknown, known_male, known_female, known_other = 0, 0, 0, 0

    # 遍历
    for user in friends:
        # 备注不为空
        if((user.remark_name).strip()):
            if(user.sex == 1):
                known_male += 1
            elif(user.sex == 2):
                known_female += 1
            else:
                known_other += 1
        else:
            unknown += 1

    name_list = ['未设置备注的好友', '设置备注的男性好友', '设置备注的女性好友', '设置备注的其他好友']
    num_list = [unknown, known_male, known_female, known_other]

    pie = Pie()
    pie.add("你认识的好友比例", [list(z) for z in zip(name_list, num_list)])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="你认识的好友比例"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render('data/你认识的好友比例.html')


# 分析备注名称
def analyze_remark_name():
    close_partner_dict = {'宝宝,猪,仙女,亲爱,老婆':0, '老公':0, '父亲,爸':0, '母亲,妈':0, '闺蜜,死党,基友':0}

    # 遍历好友数据
    for user in friends:
        for key in close_partner_dict.keys():
            # 判断该好友备注名是否包含close_partner_dict中的任意一个key
            name = key.split(',')
            for sub_name in name:
                if(sub_name in user.remark_name):
                    close_partner_dict[key] += 1
                    break


    name_list = ['最重要的她', '最重要的他', '爸爸', '妈妈', '死党']
    num_list = [x for x in close_partner_dict.values()]

    pie = Pie()
    pie.add("可能是你最亲密的人", [list(z) for z in zip(name_list, num_list)])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="可能是你最亲密的人"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render('data/你最亲密的人.html')



# 分析个性签名
def analyze_signature():

    # 个性签名列表
    data = []
    for user in friends:

        # 清除签名中的微信表情emoj，即<span class.*?</span>
        # 使用正则查找并替换方式，user.signature为源文本，将<span class.*?</span>替换成空
        new_signature = re.sub(re.compile(r"<span class.*?</span>", re.S), "", user.signature)

        # 只保留签名为1行的数据，过滤为多行的签名
        if(len(new_signature.split('\n')) == 1):
            data.append(new_signature)

    # 将个性签名列表转为string
    data = '\n'.join(data)

    # 进行分词处理，调用接口进行分词
    # 这里不使用jieba或snownlp的原因是无法打包成exe文件或者打包后文件非常大
    postData = {'data':data, 'type':'exportword', 'arg':'', 'beforeSend':'undefined'}
    response = post('http://life.chacuo.net/convertexportword',data=postData)
    data = response.text.replace('{"status":1,"info":"ok","data":["', '')
    # 解码
    data = data.encode('utf-8').decode('unicode_escape')

    # 将返回的分词结果json字符串转化为python对象，并做一些处理
    data = data.split("=====================================")[0]

    # 将分词结果转化为list，根据分词结果，可以知道以2个空格为分隔符
    data = data.split('  ')

    # 对分词结果数据进行去除一些无意义的词操作
    stop_words_list = [',', '，', '、', 'the', 'a', 'is', '…', '·', 'э', 'д', 'э', 'м', 'ж', 'и', 'л', 'т', 'ы', 'н', 'з', 'м', '…', '…', '…', '…', '…', '、', '.', '。', '!', '！', ':', '：', '~', '|', '▽', '`', 'ノ', '♪', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\'', '‘', '’', '“', '”', '的', '了', '是', '你', '我', '他', '她','=', '\r', '\n', '\r\n', '\t', '以下关键词', '[', ']', '{', '}', '(', ')', '（', '）', 'span', '<', '>', 'class', 'html', '?', '就', '于', '下', '在', '吗', '嗯']
    tmp_data = []
    for word in data:
        if(word not in stop_words_list):
            tmp_data.append(word)
    data = tmp_data


    # 进行词频统计，结果存入字典signature_dict中
    signature_dict = {}
    for index, word in enumerate(data):

        print(u'正在统计好友签名数据，进度%d/%d，请耐心等待……' % (index + 1, len(data)))

        if(word in signature_dict.keys()):
            signature_dict[word] += 1
        else:
            signature_dict[word] = 1

    # 开始绘制词云
    name = [x for x in signature_dict.keys()]
    value = [x for x in signature_dict.values()]
    wordcloud = WordCloud()
    wordcloud.add('微信好友个性签名词云图', [list(z) for z in zip(name, value)], word_size_range=[1,100], shape='star')
    wordcloud.render('data/好友个性签名词云.html')


# 下载好友头像，此步骤消耗时间比较长
def download_head_image(thread_name):

    # 队列不为空的情况
    while(not queue_head_image.empty()):
        # 取出一个好友元素
        user = queue_head_image.get()

        # 下载该好友头像，并保存到指定位置，生成一个15位数的随机字符串
        random_file_name = ''.join([str(random.randint(0,9)) for x in range(15)])
        user.get_avatar(save_path='image/' + random_file_name + '.jpg')

        # 输出提示
        print(u'线程%d:正在下载微信好友头像数据，进度%d/%d，请耐心等待……' %(thread_name, len(friends)-queue_head_image.qsize(), len(friends)))




# 生成一个html文件，并保存到文件file_name中
def generate_html(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        data = '''
            <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
            <meta charset="UTF-8">
            <title>一键生成微信个人专属数据报告(了解你的微信社交历史)</title>
            <meta name='keywords' content='微信个人数据'>
            <meta name='description' content=''> 

            
            <iframe name="iframe1" marginwidth=0 marginheight=0 width=100% height=60% src="data/好友地区分布.html" frameborder=0></iframe>
            <iframe name="iframe2" marginwidth=0 marginheight=0 width=100% height=60% src="data/某省好友地区分布.html" frameborder=0></iframe>
            <iframe name="iframe3" marginwidth=0 marginheight=0 width=100% height=60% src="data/好友性别比例.html" frameborder=0></iframe>
            <iframe name="iframe4" marginwidth=0 marginheight=0 width=100% height=60% src="data/你认识的好友比例.html" frameborder=0></iframe>
            <iframe name="iframe5" marginwidth=0 marginheight=0 width=100% height=60% src="data/你最亲密的人.html" frameborder=0></iframe>
            <iframe name="iframe6" marginwidth=0 marginheight=0 width=100% height=60% src="data/特殊好友分析.html" frameborder=0></iframe>
            <iframe name="iframe7" marginwidth=0 marginheight=0 width=100% height=60% src="data/共同所在群聊分析.html" frameborder=0></iframe>
            <iframe name="iframe8" marginwidth=0 marginheight=0 width=100% height=60% src="data/好友个性签名词云.html" frameborder=0></iframe>
            <iframe name="iframe9" marginwidth=0 marginheight=0 width=100% height=60% src="data/微信好友头像拼接图.html" frameborder=0></iframe>
            <iframe name="iframe10" marginwidth=0 marginheight=0 width=100% height=60% src="data/使用人脸的微信好友头像拼接图.html" frameborder=0></iframe>
        '''
        f.write(data)



# 初始化所需文件夹
def init_folders():
    if(not (exists('image'))):
        makedirs('image')
    else:
        rmtree('image')
        makedirs('image')

    if(not (exists('data'))):
        makedirs('data')
    else:
        rmtree('data')
        makedirs('data')



# 拼接所有微信好友头像
def merge_head_image():
    # 拼接头像
    pics = listdir('image')  # 得到user目录下的所有文件，即各个好友头像
    numPic = len(pics)
    eachsize = int(math.sqrt(float(640 * 640) / numPic))  # 先圈定每个正方形小头像的边长，如果嫌小可以加大
    numrow = int(640 / eachsize)
    numcol = int(numPic / numrow)  # 向下取整
    toImage = Image.new('RGB', (eachsize * numrow, eachsize * numcol))  # 先生成头像集模板

    x = 0  # 小头像拼接时的左上角横坐标
    y = 0  # 小头像拼接时的左上角纵坐标

    for index, i in enumerate(pics):

        print(u'正在拼接微信好友头像数据，进度%d/%d，请耐心等待……' % (index + 1, len(pics)))

        try:
            # 打开图片
            img = Image.open('image/' + i)
        except IOError:
            print(u'Error: 没有找到文件或读取文件失败')
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



# 检测使用真实人脸的好友个数
def detect_human_face():

    # 得到user目录下的所有文件名称，即各个好友头像
    pics = listdir('image')

    # 使用人脸的头像个数
    count_face_image = 0

    # 存储使用人脸的头像的文件名
    list_name_face_image = []

    # 加载人脸识别模型
    face_cascade = CascadeClassifier('model/haarcascade_frontalface_default.xml')

    for index, file_name in enumerate(pics):
        print(u'正在进行人脸识别，进度%d/%d，请耐心等待……' % (index+1, len(pics)))
        # 读取图片
        img = imread('image/' + file_name)

        # 检测图片是否读取成功，失败则跳过
        if img is None:
            continue

        # 对图片进行灰度处理
        gray = cvtColor(img, COLOR_BGR2GRAY)
        # 进行实际的人脸检测，传递参数是scaleFactor和minNeighbor,分别表示人脸检测过程中每次迭代时图
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if (len(faces) > 0):
            count_face_image += 1
            list_name_face_image.append(file_name)

    print(u'使用人脸的头像%d/%d' %(count_face_image,len(pics)))



    # 开始拼接使用人脸的头像
    pics = list_name_face_image
    numPic = len(pics)
    eachsize = int(math.sqrt(float(640 * 640) / numPic))  # 先圈定每个正方形小头像的边长，如果嫌小可以加大
    numrow = int(640 / eachsize)
    numcol = int(numPic / numrow)  # 向下取整
    toImage = Image.new('RGB', (eachsize * numrow, eachsize * numcol))  # 先生成头像集模板

    x = 0  # 小头像拼接时的左上角横坐标
    y = 0  # 小头像拼接时的左上角纵坐标

    for index, i in enumerate(pics):

        print(u'正在拼接使用人脸的微信好友头像数据，进度%d/%d，请耐心等待……' %(index+1,len(pics)))
        try:
            # 打开图片
            img = Image.open('image/' + i)
        except IOError:
            print(u'Error: 没有找到文件或读取文件失败')
        else:
            # 缩小图片
            img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
            # 拼接图片
            toImage.paste(img, (x * eachsize, y * eachsize))
            x += 1
            if x == numrow:
                x = 0
                y += 1

    toImage.save('data/使用人脸的拼接' + ".jpg")


    # 生成一个网页
    with open('data/使用人脸的微信好友头像拼接图.html', 'w', encoding='utf-8') as f:
        data = '''
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                  <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
                  <meta charset="utf-8" /> 
                  <title>使用人脸的微信好友头像拼接图</title> 
            </head>
            <body>
                <p><font size=4px><strong>描述内容</strong></font></p>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <img src="使用人脸的拼接.jpg" />
            </body>
            </html>
        '''

        data = data.replace('描述内容','在{}个好友中，有{}个好友使用真实的人脸作为头像'.format(len(friends), count_face_image))
        f.write(data)


# 特殊好友分析
def analyze_special_friends():

    # 星标好友(很重要的人), 不让他看我的朋友圈的好友, 不看他朋友圈的好友, 消息置顶好友, 陌生人
    star_friends, hide_my_post_friends, hide_his_post_friends, sticky_on_top_friends, stranger_friends = 0, 0, 0, 0, 0

    for user in friends:


        # 星标好友为1,为0表示非星标,不存在星标选项的为陌生人
        if('StarFriend' in (user.raw).keys()):
            if((user.raw)['StarFriend'] == 1):
                star_friends += 1
        else:
            stranger_friends += 1

        # 好友类型及权限：1和3好友，259和33027不让他看我的朋友圈，65539和65537和66051不看他的朋友圈，65795两项设置全禁止, 73731陌生人
        if((user.raw)['ContactFlag'] in [259, 33027, 65795]):
            hide_my_post_friends += 1
        if ((user.raw)['ContactFlag'] in [66051, 65537, 65539, 65795]):
            hide_his_post_friends += 1

        # 消息置顶好友为2051
        if ((user.raw)['ContactFlag'] in [2051]):
            sticky_on_top_friends += 1

        # 陌生人
        if ((user.raw)['ContactFlag'] in [73731]):
            stranger_friends += 1


    bar = Bar()
    bar.add_xaxis(['星标', '不让他看我朋友圈', '不看他朋友圈', '消息置顶', '陌生人'])
    bar.add_yaxis('特殊好友分析', [star_friends, hide_my_post_friends, hide_his_post_friends, sticky_on_top_friends, stranger_friends])
    bar.render('data/特殊好友分析.html')



# 共同所在群聊成员分析
def group_common_in():

    # 获取所有活跃的群聊
    groups = bot.groups()

    # 每个好友与你相同的群聊个数
    dict_common_in = {}

    # 遍历所有好友，第0个为你自己，所以去掉
    for x in friends[1:]:
        # 依次在每个群聊中搜索
        for y in groups:
            # x在y中
            if(x in y):
                # 获取微信名称
                name = x.nick_name
                # 判断是否有备注，有的话就使用备注
                if(x.remark_name and x.remark_name != ''):
                    name = x.remark_name

                # 增加计数
                if(name in dict_common_in.keys()):
                    dict_common_in[name] += 1
                else:
                    dict_common_in[name] = 1

    # 从dict_common_in结果中取出前n大个数据
    n = 0

    if(len(dict_common_in) > 5):
        n = 6
    elif(len(dict_common_in) > 4):
        n = 5
    elif(len(dict_common_in) > 3):
        n = 4
    elif(len(dict_common_in) > 2):
        n = 3
    elif(len(dict_common_in) > 1):
        n = 2
    elif(len(dict_common_in) > 0):
        n = 1

    # 排序，并转化为list
    sort_list = sorted(dict_common_in.items(), key=lambda item: item[1], reverse=True)

    # 取出前n大的值
    sort_list = sort_list[:n]

    bar = Bar()
    bar.add_xaxis([x[0] for x in sort_list])
    bar.add_yaxis("共同所在群聊分析", [x[1] for x in sort_list])
    bar.render('data/共同所在群聊分析.html')


# 运行前，请先确保安装了所需库文件
# 若没安装，请执行以下命令:pip install -r requirement.txt
if __name__ == '__main__':

    # 初始化所需文件夹
    init_folders()


    # 启动微信机器人，自动根据操作系统执行不同的指令
    if('Windows' in system()):
        # Windows
        bot = Bot()
    elif('Darwin' in system()):
        # MacOSX
        bot = Bot(cache_path=True)
    elif('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2,cache_path=True)
    else:
        # 自行确定
        print(u"无法识别你的操作系统类型，请自己设置")
        exit()


    # 获取好友数据
    print(u'正在获取微信好友数据信息，请耐心等待……')
    friends = bot.friends(update=False)
    # i.nick_name, i.remark_name, i.sex, i.province, i.city, i.signature
    print(u'微信好友数据信息获取完毕\n')


    print(u'正在分析你的群聊，请耐心等待……')
    group_common_in()
    print(u'分析群聊完毕\n')


    print(u'正在获取微信好友头像信息，请耐心等待……')
    # 创建一个队列，用于多线程下载头像，提高下载速度
    queue_head_image = Queue()

    # 将每个好友元素存入队列中
    # 如果为了方便调试，可以仅仅插入几个数据，friends[1:10]
    for user in friends:
        queue_head_image.put(user)

    # 启动10个线程下载头像
    for i in range(1, 10):
        t = Thread(target=download_head_image,args=(i,))
        t.start()
    print(u'微信好友头像信息获取完毕\n')


    print(u'正在分析好友性别比例，请耐心等待……')
    sex_ratio()
    print(u'分析好友性别比例完毕\n')


    print(u'正在分析好友地区分布，请耐心等待……')
    region_distribution()
    print(u'分析好友地区分布完毕\n')

    print(u'正在统计你认识的好友，请耐心等待……')
    statistics_friends()
    print(u'统计你认识的好友完毕\n')

    print(u'正在分析你最亲密的人，请耐心等待……')
    analyze_remark_name()
    print(u'分析你最亲密的人完毕\n')

    print(u'正在分析你的特殊好友，请耐心等待……')
    analyze_special_friends()
    print(u'分析你的特殊好友完毕\n')

    print(u'正在分析你的好友的个性签名，请耐心等待……')
    analyze_signature()
    print(u'分析你的好友的个性签名完毕\n')




    # 由于下载头像是多线程进行，并且存在可能下载时间比较久的情况
    # 所以当我们完成所有其他功能以后，需要等待微信好友头像数据下载完毕后再进行操作
    while(not queue_head_image.empty()):
        sleep(1)

    print(u'正在拼接所有微信好友头像数据，请耐心等待……')
    merge_head_image()
    print(u'拼接所有微信好友头像数据完毕\n')

    print(u'正在检测使用人脸作为头像的好友数量，请耐心等待……')
    detect_human_face()
    print(u'检测使用人脸作为头像的好友数量完毕\n')


    # 生成一份最终的html文件
    print(u'所有数据获取完毕，正在生成微信个人数据报告，请耐心等待……')
    generate_html('微信个人数据报告.html')
    print(u'生成微信个人数据报告完毕，该文件为当前目录下的[微信个人数据报告.html]\n')


    # 调用系统方式自动打开这个html文件
    print(u'已为你自动打开 微信个人数据报告.html')
    open_html('微信个人数据报告.html')
