# -*- coding:utf-8 -*-

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
