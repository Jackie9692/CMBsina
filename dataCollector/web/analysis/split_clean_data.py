# -*- coding: utf-8 -*-
# 抓取数据预处理 #
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from os import sys, path

sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))  # 引入绝对路径

from dao.baseDao import StatusDao
import jieba
import re


# 过滤函数
def filter_status(word_list):
    if word_list is None:
        return False
    word_set = set(word_list)
    if word_set is not None:
        if len(word_set) >= 3:  # 重复的词语个数不少于3个保留
            return True
    return False


if __name__ == "__main__":
    statusDao = StatusDao()
    statusItems = statusDao.queryCondition({"isValidated": None})
    for each in statusItems:
        text = each.text  # 微博文本
        # status_id = each.status_id #微博正文

        if text is None:
            continue

        text = text.decode("utf8")  # 过滤中英文符号
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）:：]+".decode("utf8"), "".decode("utf8"), text)

        # print(text + "\n")
        targetText_list = list(jieba.cut(text, cut_all=False))  # 精确模式生成分词


        targetText = ",".join(targetText_list)
        each.jieba_text = targetText
        if filter_status(targetText_list):  # 通过过滤词语
            each.isValidated = True
            statusDao.updateByItem(each)
        else:
            each.isValidated = False
            statusDao.updateByItem(each)





