# -*-coding:utf-8-*-
from sqlalchemy import Column, Integer, String, Time, BigInteger, DateTime, Boolean, Float
from sqlalchemy.dialects.mysql.base import TEXT

from dao import Base


# 微博状态条信息
class Status(Base):
    __tablename__ = "status"
    status_id = Column(BigInteger, primary_key=True, nullable=False)  # ID
    user_id = Column(Integer)  # 用户id
    text = Column(TEXT, nullable=False)  # 微博文本
    create_date = Column(DateTime)  # 创建日期
    userurl = Column(String(255))  # 用户主页URL
    source = Column(String(20))  # 微博客户端 web、iphone、Android
    repost_count = Column(Integer)  # 转发数
    comments_count = Column(Integer)  # 评论数
    emotion = Column(String(20), default=None)  # 情绪
    statusurl = Column(String(255))  # 微博链接
    geo = Column(String(255))  # 发微博地址信息
    pic_urls = Column(TEXT)  # 图片URL
    collect_by_keywords = Column(TEXT)  # 匹配关键字
    collect_date = Column(DateTime)  # 爬取的时间戳
    jieba_text = Column(TEXT)  #结巴分词文本
    isValidated = Column(Boolean, default=None)  #默认未被检验



#微博评论信息
class Comment(Base):
    __tablename__ = "comment"
    comment_id = Column(BigInteger, primary_key=True, nullable=False)  #评论主键
    user_id = Column(BigInteger)  #评论人id
    status_id = Column(BigInteger)  #微博id
    text = Column(TEXT)  #评论内容
    create_date = Column(DateTime)  #评论时间
    emotion = Column(String(255))  #情绪判定
    collect_date = Column(DateTime)  #爬取时间


#用户信息
class User(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True, nullable=False)  # 用户ID
    user_name = Column(String(255))  # 用户名
    friends_count = Column(Integer)  # 关注数
    followers_count = Column(Integer)  # 被关注数
    statuses_count = Column(Integer)  # 微博数
    collect_date = Column(Integer)  # 爬取时间戳

    def tojson(self):
        user = {'name': self.Name, 'user_id': self.user_id, 'friends_count': self.friends_count,
                'followers_count': self.followers_count, 'status_count': self.statuses_count,
                'timestamp': self.timestamp}
        return user

