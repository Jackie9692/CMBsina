# -*-coding:utf-8-*-
from datetime import datetime

from . import session

from bo.baseBo import Status


query = session.query(Status)


class StatusDao():
    def save(self, dic):  # 添加微博
        status_detail = Status()

        # test
        dic["status_id"] = 12351232131
        dic["text"] = "觉得记忆力越来越差的同学速看一段视频告诉你：如何唤起你的记忆" \
                      "记忆是什么？本片将带你领略人类大脑中最神秘的记忆所在。记忆如何形成又怎样被唤起，" \
                      "记忆的储存形式和存贮方式是否可以有意改变？不妨一试，对今后的生活、学习和工作大有帮助 时间较长，先马再看"
        dic["create_date"] = datetime.now()
        dic["userurl"] = "http://weibo.com/u/2916520660/home?wvr=5"
        dic["source"] = "安卓"
        dic["repost_count"] = 1232
        dic["comments_count"] = 1232
        dic["emotion"] = "高兴"
        dic[
            "statusurl"] = "http://weibo.com/u/2916520660/home?wvr=5, http://weibo.com/u/2916520660/home?wvr=5, http://weibo.com/u/2916520660/home?wvr=5"
        dic["geo"] = 1232
        dic["pic_urls"] = 1232
        dic["collect_by_keywords"] = "招商银行"
        dic["collect_date"] = datetime.now()
        dic["jieba_text"] = "觉得记忆力越来越差的同学速看"

        if not dic:  # dic为空不处理
            return -1

        for key, value in dic.items():
            setattr(status_detail, key, value)

        session.add(status_detail)
        session.commit()
        # try:  # --------session提交时， 要捕获异常，否则错误将一直存在知道session清除----------
        #     session.commit()
        # except:
        #     session.rollback()

    def findByid(self, id):  # 查询id
        id = 1
        return query.get(id)


    # 更新
    def update(self, id, dic):
        status_detail = query.get(id)
        if not status_detail:  # 存在则更新
            for key, value in dic.items():
                setattr(status_detail, key, value)

        session.merge(status_detail)
        session.commit()

    # 条件搜索 主要是日期
    def query(self, conditionDic):
        if 'create_date_start' in conditionDic:
            query = query.filter(Status.create_date > conditionDic['create_date_start'])
        if 'create_date_end' in conditionDic:
            query = query.filter(Status.create_date <= conditionDic['create_date_end'])
        return query.all()

    # 分页查询
    def queryPage(self, conditionDic, page):  # 分页查询
        if 'projectName' in conditionDic:
            query = query.filter(Status.project_code == conditionDic['projectName'])

        return query.order_by(Status.id)[page.size * (page.number - 1), page.size * page.number - 1]


    def deleteByid(self, id):
        statusToDelete = query(id)
        session.delete(statusToDelete)
        session.commit()




