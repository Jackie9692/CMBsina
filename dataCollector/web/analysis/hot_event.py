# -*- coding: utf-8 -*-


# 统计每日热词和关键事件 #
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from os import sys, path

sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))  # 引入绝对路径

from dao.baseDao import StatusDao

import datetime



# 噪声词 需要人工建立
noise_words_list = ["招行", "招商银行", "明天"]
# 最热词数量
top_hot_words__num = 4
#所有词字典
words_dic = {}


# 创建文本词语数字典
def build_words_dic(word_list):
    for each in word_list:
        each = str(each)
        if each in words_dic.keys():
            words_dic[each] += 1
        else:
            words_dic[each] = 1

    return words_dic


def find_top_words(targetNum):
    target_dic = {}
    count = 0
    for key, value in sorted(words_dic.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        if count < targetNum:
            if key not in dict():
                target_dic[key] = value
            count += 1
    return target_dic





#产生最近一周列表 不包含当天
def datelist():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(7)


    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append(curr_date)
        curr_date += datetime.timedelta(1)
    # result.append(curr_date)
    return result


#产生关联系词
def generate_top_events():
    pass


# if __name__ == '__main__':
#     myDat = loadDataSet()  # 导入数据集
#     # C1 = createC1( myDat )                                  # 构建第一个候选项集列表C1
#     # D = map( set, myDat )                                   # 构建集合表示的数据集 D，python3中的写法，或者下面那种
#     # D=[var for var in map(set,myDat)]
#     # D=[set(var) for var in myDat] #D: [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]
#     # L, suppData = scanD( D, C1, 0.5 )                       # 选择出支持度不小于0.5 的项集作为频繁项集
#     # print(u"频繁项集L：", L)
#     # print(u"所有候选项集的支持度信息：", suppData)
#     # print("myDat",myDat)
#     L, suppData = apriori(myDat, 0.5)  # 选择频繁项集
#     print(u"频繁项集L：", L)
#     print(u"所有候选项集的支持度信息：", suppData)
#     rules = generateRules(L, suppData, minConf=0.7)
#     print('rules:\n', rules)


if __name__ == "__main__":
    statusDao = StatusDao()
    # statusItems = statusDao.queryCondition({"isValidated": True, "create_date_start": "", "create_date_end": "", })

    for date in datelist():
        # 过滤条件
        filterCondition = {"isValidated": True, "date": date}
        statusItems = statusDao.queryCondition(filterCondition)

        words_dic = {}  #字典初始化为空
        for each in statusItems:
            jieba_text = each.jieba_text  # 微博分词文本
            if jieba_text is None:
                continue
            jiba_text_list = jieba_text.split(",")

            build_words_dic(jiba_text_list)


        #top词字典
        target_dic = find_top_words(top_hot_words__num)

        D = [[1, 3, 4, 5], [2, 3, 5], [1, 2, 3, 4, 5], [2, 3, 4, 5]]
        F = apriori(D, 0.5)
        print '\nfrequent itemset:\n', F

        pass #关联性分析热词 查表统计情绪
        #当日热词保存起来




    #
    # for key, value in target_dic.iteritems():
    #     print "%s: %s" % (key, value)
    # print("hahha")
    # print datelist()









