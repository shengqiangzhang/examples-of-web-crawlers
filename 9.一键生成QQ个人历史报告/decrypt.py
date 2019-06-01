# -*- coding:utf-8 -*-

# 引用第三方库
from execjs import compile


# 对qrsig进行基本的加密，该加密函数由抓包获得，需要具备一定抓包知识才能找到该加密函数
# 根据javascript版的加密函数，将其改写成python版本
def hash33_token(t):
    e, n = 0, len(t)
    for i in range(0,n):
        e += (e << 5) + ord(t[i])

    return 2147483647 & e



# 对skey进行基本的加密，该加密函数由抓包获得，需要具备一定抓包知识才能找到该加密函数
# 根据javascript版的加密函数，将其改写成python版本
def hash33_bkn(skey):
    e = skey
    t = 5381

    for n in range(0,len(e)):
        t += (t << 5) + ord(e[n])

    return 2147483647 & t



# 加载js文件
def get_js(js_name):
    with open(js_name, 'r', encoding='UTF-8') as f:
        # 一般js文件不大，不会超出计算机的内存，所以直接一次性读取全部数据
        js_data = f.read()
        return js_data



# 获取sck的值，该加密函数由抓包获得，需要具备一定抓包知识才能找到该加密函数
# 由于该js代码较长，所以不转化为python版本，而是采取直接调用js文件中的函数
def get_sck(skey):

    # 读取js脚本
    md5 = get_js('decrypt/md5.js')

    # 加载js脚本引擎
    ctx = compile(md5)

    # 调用js脚本中某个函数
    # 第1个参数为函数名，第2到第n个参数为该函数依次所需的参数
    result = ctx.call('hex_md5', str(skey))

    return str(result)


# 获取g_tk值，这里的g_tk值算法由vip.qq.com获取，暂不清楚是否能直接用于其他域名
def get_csrf_token(skey):
    # 读取js脚本
    js = get_js('decrypt/getCSRFToken.js')

    # 加载js脚本引擎
    ctx = compile(js)

    # 调用js脚本中某个函数
    # 第1个参数为函数名，第2到第n个参数为该函数依次所需的参数
    tmp_data = ctx.call('getCSRFToken', str(skey))


    # 读取js脚本
    js = get_js('decrypt/md5.js')

    # 加载js脚本引擎
    ctx = compile(js)

    # 调用js脚本中某个函数
    # 第1个参数为函数名，第2到第n个参数为该函数依次所需的参数
    result = ctx.call('hex_md5', str(tmp_data))

    return result