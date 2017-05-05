# coding:utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from controller import handler

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

handlers = [
    (r"/status/add", handler.StatusAdd),  # 微博写入测试
    (r"/status/delete", handler.StatusDelete),
    (r"/status/checkByID", handler.StatusCheckByID),
    (r"/status/pageQuery", handler.StatusPageQuery),

    (r"/comment/add", handler.CommentAdd),  # 微博评论写入测试
    (r"/comment/delete", handler.CommentDelete),
    (r"/comment/checkByID", handler.CommentCheckByID),
    (r"/comment/pageQuery", handler.CommentPageQuery),


    (r"/user/add", handler.UserAdd),  # 微博用户写入测试
    (r"/user/delete", handler.UserDelete),
    (r"/user/checkByID", handler.UserCheckByID),
    (r"/user/pageQuery", handler.UserPageQuery),
]

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=handlers,
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
