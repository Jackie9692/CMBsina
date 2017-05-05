# -*-coding:utf-8-*-
from datetime import datetime
import random

from . import session

from bo.baseBo import Status
from bo.baseBo import Comment
from bo.baseBo import User




# ****微博***#
class StatusDao():
    def __init__(self):
        self.query = session.query(Status)

    def save(self, dic):  # 添加微博
        status_detail = Status()

        # test
        dic["status_id"] = random.randint(1, 1000000)
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
        # dic["isValidated"] = False

        if not dic:  # dic为空不处理
            return -1

        for key, value in dic.items():
            setattr(status_detail, key, value)

        try:  # --------session提交时， 要捕获异常，否则错误将一直存在知道session清除----------
            session.add(status_detail)
            session.commit()
        except:
            session.rollback()
            raise


    def findByid(self, id):  # 查询id
        return self.query.get(id)


    # 更新
    def update(self, id, dic):
        status_detail = query.get(id)
        if not status_detail:  # 存在则更新
            for key, value in dic.items():
                setattr(status_detail, key, value)

        try:
            session.merge(status_detail)
            session.commit()
        except:
            session.rollback()
            raise


    # 更新
    def updateByItem(self, statusItem):
        if statusItem is None:
            return -1
        try:
            session.merge(statusItem)
            session.commit()
        except:
            session.rollback()
            raise

    # 条件搜索 主要是日期
    def queryCondition(self, conditionDic):
        query = self.query
        if 'create_date_start' in conditionDic:
            query = query.filter(Status.create_date > conditionDic['create_date_start'])
        if 'create_date_end' in conditionDic:
            query = query.filter(Status.create_date <= conditionDic['create_date_end'])
        if "isValidated" in conditionDic:
            query = query.filter(Status.isValidated == conditionDic["isValidated"])
        if "emotion" in conditionDic:
            query = query.filter(Status.isValidated == conditionDic["emotion"])
        return query.all()

    # 分页查询
    def queryPage(self, conditionDic, page):
        if 'projectName' in conditionDic:
            query = self.query.filter(Status.project_code == conditionDic['projectName'])

        return query.order_by(Status.id)[page.size * (page.number - 1), page.size * page.number - 1]


    def deleteByid(self, id):
        statusToDelete = self.query.get(id)
        try:
            session.delete(statusToDelete)
            session.commit()
        except:
            session.rollback()
            raise


# ****评论***#
class CommentDao():
    def __init__(self):
        self.query = session.query(Comment)

    def save(self, dic):  # 添加微博
        comment_detail = Comment()

        # test
        dic["comment_id"] = random.randint(1, 1000000)
        dic["user_id"] = 1235123213111
        dic["status_id"] = 1235123213111
        dic["text"] = "这是一条很开心的评论"
        dic["create_date"] = datetime.now()
        dic["emotion"] = 1232
        dic["collect_date"] = datetime.now()

        if not dic:  # dic为空不处理
            return -1

        for key, value in dic.items():
            setattr(comment_detail, key, value)

        try:
            session.flush()
            session.add(comment_detail)
            session.commit()
        except:
            session.rollback()
            raise

    def findByid(self, id):  # 查询id
        return self.query.get(id)


    # 更新
    def update(self, id, dic):
        comment_detail = self.query.get(id)
        if not comment_detail:  # 存在则更新
            for key, value in dic.items():
                setattr(comment_detail, key, value)

        try:
            session.merge(comment_detail)
            session.commit()

        except:
            session.rollback()
            raise


    # 条件搜索 主要是日期
    def query(self, conditionDic):
        if 'create_date_start' in conditionDic:
            query = self.query.filter(Comment.create_date > conditionDic['create_date_start'])
        if 'create_date_end' in conditionDic:
            query = query.filter(Comment.create_date <= conditionDic['create_date_end'])
        return query.all()


    # 分页查询
    def queryPage(self, conditionDic, page):  # 分页查询
        if 'projectName' in conditionDic:
            query = self.query.filter(Comment.project_code == conditionDic['projectName'])

        return query.order_by(Comment.id)[page.size * (page.number - 1), page.size * page.number - 1]


    def deleteByid(self, id):
        commentToDelete = self.query.get(id)
        try:
            session.delete(commentToDelete)
            session.commit()
        except:
            session.rollback()
            raise


# ****评论***#
class UserDao():
    def __init__(self):
        self.query = session.query(User)

    def save(self, dic):  # 添加微博
        user_detail = User()

        # test
        dic["user_id"] = random.randint(1, 1000000)
        dic["user_name"] = "Jackie"
        dic["friends_count"] = random.randint(1, 1000000)
        dic["followers_count"] = random.randint(1, 1000000)
        dic["statuses_count"] = random.randint(1, 1000000)
        dic["collect_date"] = datetime.now()

        if not dic:  # dic为空不处理
            return -1

        for key, value in dic.items():
            setattr(user_detail, key, value)

        try:
            session.add(user_detail)
            session.commit()
        except:
            session.rollback()
            raise

    def findByid(self, id):  # 查询id
        return self.query.get(id)


    # 更新
    def update(self, id, dic):
        user_detail = self.query.get(id)
        if not user_detail:  # 存在则更新
            for key, value in dic.items():
                setattr(user_detail, key, value)

        try:
            session.merge(user_detail)
            session.commit()
        except:
            session.rollback()
            raise

    # 条件搜索 主要是日期
    def query(self, conditionDic):
        if 'create_date_start' in conditionDic:
            query = self.query.filter(User.create_date > conditionDic['create_date_start'])
        if 'create_date_end' in conditionDic:
            query = query.filter(User.create_date <= conditionDic['create_date_end'])
        return query.all()

    # 分页查询
    def queryPage(self, conditionDic, page):  # 分页查询
        if 'projectName' in conditionDic:
            query = self.query.filter(User.project_code == conditionDic['projectName'])

        return query.order_by(User.id)[page.size * (page.number - 1), page.size * page.number - 1]


    def deleteByid(self, id):
        userToDelete = self.query.get(id)
        try:
            session.delete(userToDelete)
            session.commit()
        except:
            session.rollback()
            raise