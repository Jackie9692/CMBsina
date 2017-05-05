# coding:utf-8

# Controller 层#
from tornado.web import RequestHandler as RHandler

from dao.baseDao import StatusDao
from dao.baseDao import CommentDao
from dao.baseDao import UserDao



# 微博新增
class StatusAdd(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.statusDao = StatusDao()

    def get(self):
        self.statusDao.save({})
        self.write("add success!")


# 微博删除接口
class StatusDelete(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.statusDao = StatusDao()

    def get(self):
        status_id = self.get_argument("id", None)
        self.statusDao.deleteByid(status_id)
        self.write("delete success!")


# 微博查询接口
class StatusCheckByID(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.statusDao = StatusDao()

    def get(self):
        status_id = self.get_argument("id", None)
        status = self.statusDao.findByid(int(status_id))
        self.render("statusDetail.html", status=status)


# 微博分页查询
class StatusPageQuery(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.statusDao = StatusDao()

    def get(self):
        status_id = self.get_argument("status_id", None)
        status = self.statusDao.findByid(status_id)
        self.render("statusDetail.html", status=status)


# *********************************************************微博评论**************************************************#
# 微博评论新增
class CommentAdd(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.commentDao = CommentDao()

    def get(self):
        self.commentDao.save({})
        self.write("add success!")


# 微博评论删除接口
class CommentDelete(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.commentDao = CommentDao()

    def get(self):
        comment_id = self.get_argument("id", None)
        self.commentDao.deleteByid(int(comment_id))
        self.write("delete success!")


# 微博评论查询接口
class CommentCheckByID(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.commentDao = CommentDao()

    def get(self):
        comment_id = self.get_argument("id", None)
        comment = self.commentDao.findByid(int(comment_id))
        self.render("commentDetail.html", comment=comment)


#微博评论分页查询
class CommentPageQuery(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.commentDao = CommentDao()

    def get(self):
        comment_id = self.get_argument("comment_id", None)
        comment = self.commentDao.findByid(comment_id)
        self.render("commentDetail.html", comment=comment)


#*********************************************************微博用户**************************************************#

# 微博用户新增
class UserAdd(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.userDao = UserDao()

    def get(self):
        self.userDao.save({})
        self.write("add success!")


# 微博用户删除接口
class UserDelete(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.userDao = UserDao()

    def get(self):
        user_id = self.get_argument("id", None)
        self.userDao.deleteByid(user_id)
        self.write("delete success!")


#微博用户查询接口
class UserCheckByID(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.userDao = UserDao()

    def get(self):
        user_id = self.get_argument("id", None)
        user = self.userDao.findByid(int(user_id))
        self.render("userDetail.html", user=user)


#微博用户分页查询
class UserPageQuery(RHandler):
    def __init__(self, application, request):
        RHandler.__init__(self, application, request)
        self.userDao = UserDao()

    def get(self):
        user_id = self.get_argument("user_id", None)
        user = self.userDao.findByid(user_id)
        self.render("userDetail.html", user=user)




