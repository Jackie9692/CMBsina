# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# import sched
# import sys
# import os.path
# script_path = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(os.path.join(script_path, '..'))
# import zope.testing.loggingsupport
# import zc.lockfile
# from dataCollector.apiCollector.weiboSensor import *
# from dataCollector.dataMerger.statusMerger import *
# from dataCollector.commentsUpdater.commentsUpdate import *
#
# dataCollectorScheduler = sched.scheduler(time.time, time.sleep)
# if __name__ == "__main__":
# handler = zope.testing.loggingsupport.InstalledHandler('zc.lockfile')
# try:
# lockFile = os.path.join(script_path, "dataCollector.lck")  # 获取唯一性互斥访问文件锁
# dataCleaningScriptLock = zc.lockfile.LockFile(lockFile)
# except zc.lockfile.LockError:
# # 锁定文件失败，表明该脚本已经在执行了，不允许重复执行该脚本
# print("There is already one instance of dataCollector script running current! will exit in 3 seconds. ")
# time.sleep(3)
# sys.exit()
# else:
# start_comments_updater()    #启动comments ReCollect模块
#         start_sensor(dataCollectorScheduler)    #启动API Retrieve模块
#         mergerStart(dataCollectorScheduler) #启动Status Merge模块
#         dataCollectorScheduler.run()


# encoding=utf-8
import jieba

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易网易网易网易网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))

# seg_list = jieba.cut_for_search("小明,,,,硕士?毕业于?中国科?学院计算所，'童声梦想'后在日本京都大学深造")  # 搜索引擎模式
# print("\ ".join(seg_list))



# import re
# temp = "想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8 0. ！！？？  8 6 。0.  2。 3     有,惊,喜,哦"
# temp = temp.decode("utf8")
# string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),temp)
# print(string)


# def take (n):
#     for i in range(n):
#         yield str(i)
#
# ge = take(4)
#
# l = list(ge)
#
#
# a = ",".join(l)
#
# print a

# from time import time
#
# import urllib
# import urllib2
# import json
# import hmac
# import hashlib
#
#
# secretId = "AKIDUs6A3kManoeoqgGxUtGSSGtKYaSDBtnV"
# secretKey = "iFcpqfKyRirwLfmnsnY7Zs1yjKl283o6"
#
# content = "双万兆服务器就是好，只是内存小点"
#
# timestamp = time()
#
# # print timestamp
# timestamp_str = str(int(timestamp))
# print(timestamp_str)
#
# method = "GET"
# apiurl = "wenzhi.api.qcloud.com/v2/index.php?"
#
# #获取签名
# para_sig_list = [('Action', 'TextSentiment'), ('Nonce', 345122), ('Region', 'sh'), ('SecretId', secretId),
#                  ('Timestamp', timestamp_str)]
#
# signature_url = method + apiurl + urllib.urlencode(para_sig_list)
# print(signature_url)
# signature = hmac.new(secretKey, signature_url, hashlib.sha1).digest().encode('base64')
#
#
#
# #授权访问
# para_list = [('Action', 'TextSentiment'), ('Nonce', 345122), ('Region', 'sh'), ('SecretId', secretId),
#              ('Timestamp', timestamp_str), ('Signature', signature), ("content", content)]
#
# # para_dic = dict(para_list)
# apiurl = "https://wenzhi.api.qcloud.com/v2/index.php?"
# url = apiurl + urllib.urlencode(para_list)
#
# print(url)
# req = urllib2.Request(url)
#
# res_data = urllib2.urlopen(req)
# res = res_data.read()
#
# data = json.loads(res)
#
# for key, value in data.iteritems():
#     print(str(key) + ": " + str(value))
#
# print res


















# import base64
# import hmac
# import hashlib
#
# secretId = "AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA"
# secretKey = "Gu5t9xGARNpq86cd98joQYCN3Cozk1qA"
# srcStr = 'GETcvm.api.qcloud.com/v2/index.php?Action=DescribeInstances&Nonce=11886&Region=gz&SecretId=AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA&Timestamp=1465185768&instanceIds.0=ins-09dx96dg&limit=20&offset=0';
#
# h = hmac.new(secretKey, srcStr, hashlib.sha1)
#
# s = h.digest()
#
# signature = s.encode('base64')
#
# print(signature)


#coding=utf-8                        # 全文utf-8编码
import sys


def apriori(D, minSup):
    '''频繁项集用keys表示，
    key表示项集中的某一项，
    cutKeys表示经过剪枝步的某k项集。
    C表示某k项集的每一项在事务数据库D中的支持计数
    '''

    C1 = {}
    for T in D:
        for I in T:
            if I in C1:
                C1[I] += 1
            else:
                C1[I] = 1

    print C1
    _keys1 = C1.keys()

    keys1 = []
    for i in _keys1:
        keys1.append([i])

    n = len(D)
    cutKeys1 = []
    for k in keys1[:]:
        if C1[k[0]] * 1.0 / n >= minSup:
            cutKeys1.append(k)

    cutKeys1.sort()

    keys = cutKeys1
    all_keys = []
    while keys != []:
        C = getC(D, keys)
        cutKeys = getCutKeys(keys, C, minSup, len(D))
        for key in cutKeys:
            all_keys.append(key)
        keys = aproiri_gen(cutKeys)

    return all_keys


def getC(D, keys):
    '''对keys中的每一个key进行计数'''
    C = []
    for key in keys:
        c = 0
        for T in D:
            have = True
            for k in key:
                if k not in T:
                    have = False
            if have:
                c += 1
        C.append(c)
    return C


def getCutKeys(keys, C, minSup, length):
    '''剪枝步'''
    for i, key in enumerate(keys):
        if float(C[i]) / length < minSup:
            keys.remove(key)
    return keys


def keyInT(key, T):
    '''判断项key是否在数据库中某一元组T中'''
    for k in key:
        if k not in T:
            return False
    return True


def aproiri_gen(keys1):
    '''连接步'''
    keys2 = []
    for k1 in keys1:
        for k2 in keys1:
            if k1 != k2:
                key = []
                for k in k1:
                    if k not in key:
                        key.append(k)
                for k in k2:
                    if k not in key:
                        key.append(k)
                key.sort()
                if key not in keys2:
                    keys2.append(key)

    return keys2


D = [[ 1, 3, 4,5 ], [ 2, 3, 5 ], [ 1, 2, 3,4, 5 ], [ 2,3,4, 5 ] ]
F = apriori(D, 0.5)
print '\nfrequent itemset:\n', F