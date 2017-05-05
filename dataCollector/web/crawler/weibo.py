# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import re
import random
from selenium.webdriver.common.by import By
import threading
from collections import deque
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


LOGIN_MAX_TRIES = 10  # 登录最多尝试次数
loginURL = u"http://login.sina.com.cn/signup/signin.php?entry=sso"  # 自动登录微博的登录地址，可能会不定期改变!!
keywords_list = ['招商银行', '招行']
account_name = u"chendaxu_9692@163.com"
account_passwd = u"1152762jackie"


class Status:
    status_id = None  # ID
    user_simple = {}  # User简单信息
    text = None  # 微博文本
    date = None  # 创建日期
    userurl = None  # 用户主页URL
    source = None  # 微博客户端 web、iphone、Android
    repost_count = None  # 转发数
    comments_count = None  # 评论数
    attitude_count = None  #
    statusurl = None  # 微博链接
    geo = {}  # 微博地址信息
    pic_urls = []  # 图片URL
    keywords = []  # 匹配关键字
    timestamp = None  # 爬取的时间戳

    def tojson(self):
        status = {'status_id': self.status_id, 'user_simple': self.user_simple, 'text': self.text, 'date': self.date,
                  'userurl': self.userurl,
                  'source': self.source, 'repost_count': self.repost_count, 'comments_count': self.comments_count,
                  'attitude_count': self.attitude_count,
                  'statusurl': self.statusurl, 'keywords': self.keywords, 'pic_urls': self.pic_urls, 'geo': self.geo,
                  'timestamp': self.timestamp}
        return status


class Users:
    name = None  # 用户名
    user_id = None  # 用户ID
    friends_count = 0  # 关注数
    followers_count = 0  # 被关注数
    statuses_count = 0  # 微博数
    timestamp = None  # 爬取时间戳

    def tojson(self):
        test = {'name': self.Name, 'user_id': self.user_id, 'friends_count': self.friends_count,
                'followers_count': self.followers_count, \
                'status_count': self.statuses_count, 'timestamp': self.timestamp}
        return test


class Weibo(object):
    def __init__(self):
        self.status = Status()
        self.user = Users()

    def loginSinaWeibo(self, username, password, driver, loginUrl):

        # 自动登录
        print("Be going to Login Sina Weibo automatically!")
        loginSucess = False
        tried_times = 0
        while tried_times <= LOGIN_MAX_TRIES and not loginSucess:
            #尝试自动登录，直到登录成功或者超过最大登录次数
            tried_times += 1
            try:
                print "try login once"
                driver.get(loginUrl)
                elem_user = driver.find_element(by=By.ID, value="username")  #登录 用户名输入框
                elem_user.send_keys(username)  #fill in username
                elem_pwd = driver.find_element(by=By.ID, value="password")  #登录密码框
                elem_pwd.send_keys(password)  #fill in password
                elem_sub = driver.find_element_by_xpath('//input[@type="submit"]')
                time.sleep(0.5)
                elem_sub.click()  #click login button
                time.sleep(0.5)
                # time.sleep(5)
                loginSucess = True
                break
            except Exception as e:
                print("Error!!:" + e.message)
                if tried_times <= LOGIN_MAX_TRIES:
                    continue
                else:
                    return False
        if tried_times > 10:  #尝试登录次数超过最大次数
            return False
        else:
            # return loginSucess
            return loginSucess #登录成功

    def comeToSearchWeiboPage(self, driver):
        """
        :param driver: 浏览器
        :return:
        """
        switch_page_success = False
        try_times = 0
        while not switch_page_success and try_times <= LOGIN_MAX_TRIES / 2:
            try:
                print "try swtich to weibo homepage"
                try_times += 1
                time.sleep(3)
                weibo_link = driver.find_element_by_link_text(u"我的微博")
                weiboHomePage = weibo_link.get_attribute("href")  # http://weibo.com/
                print driver.title
                driver.get(weiboHomePage)
                switch_page_success = True
            except Exception as e:
                print("Error!:" + e.message)
        return switch_page_success

    def parse_search_page(self,keywords, driver,urlQueue):
        trytimes=0
        parseSuccess=False
        while not parseSuccess and trytimes<3:
            trytimes+=1
            try:
                # results = driver.find_elements_by_class_name("WB_cardwrap S_bg2 clearfix")
                # time.sleep(random.range(5, 10))
                time.sleep(random.randrange(5, 10))
                print "parse one page"
                # print driver.page_source
                # WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="WB_cardwrap S_bg2 clearfix"]')))
                results = driver.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]')
                # results=driver.find_elements_by_class_name("WB_cardwrap S_bg2 clearfix")
                # if isinstance(driver,webdriver.PhantomJS):
                #     driver
                # print len(results)
                # print results
                for node in results:
                    try:
                        status_content_div = node.find_element_by_xpath('.//div[@action-type="feed_list_item"]')
                        if status_content_div != []:
                            status_id = status_content_div.get_attribute("mid")  # id #status id
                            user_simple = {}  # 微博作者简要信息
                            try:
                                user_link_info = status_content_div.find_element_by_xpath('.//a[@class="W_texta W_fb"]')
                                if user_link_info != []:
                                    username = user_link_info.text.strip()
                                    userURL = user_link_info.get_attribute("href")
                                    userurl = userURL
                                    #将用户信息URL添加到共享队列中
                                    if userURL not in urlQueue:
                                        if isinstance(urlQueue, deque):
                                            urlQueue.append(userURL)
                            except Exception as e:
                                # print e.message
                                username=""
                                userurl=""
                            try:
                                status_comment = status_content_div.find_element_by_xpath('.//p[@class="comment_txt"]')
                                if  status_comment!=[]:
                                    status_text = status_comment.text.strip()
                                    # print status_text
                                #date and statusurl
                            except Exception as e:
                                status_text=""
                                # print e.message
                            try:
                                status_date_div = status_content_div.find_element_by_xpath('.//a[@node-type="feed_list_item_date"]')
                                if status_date_div !=[]:
                                    status_date = status_date_div.get_attribute("title")  # date
                                    statusurl = status_date_div.get_attribute("href")  # statusurl
                            except Exception as e:
                                # print e.message
                                status_date=""
                                status_url=""
                                # print status_date, statusurl
                            #source
                            try:
                                status_source_div = status_content_div.find_element_by_xpath('.//a[@rel="nofollow"]')
                                if status_source_div!=[]:
                                    status_source = status_source_div.get_attribute("text")  #source
                                # print status_source
                            except Exception as e:
                                    status_source=""
                                    # print e.message
                            # print status_source
                            # repost count
                            try:
                                repost_count = status_content_div.find_element_by_xpath('.//a[@action-type="feed_list_forward"]').find_element_by_tag_name('em').text
                                if repost_count != "":
                                    repost_count = repost_count
                                else:
                                    repost_count = 0
                            except:
                                repost_count = 0
                            # print repost_count
                            # comments count
                            try:
                                comments_count = status_content_div.find_element_by_xpath('.//a[@action-type="feed_list_comment"]').find_element_by_tag_name('em').text
                                if comments_count != "":
                                    comments_count = comments_count
                                else:
                                    comments_count = 0
                            except Exception, e:
                                # print "Error: ", e
                                comments_count = 0
                            # comments_count# print comments_count
                            # # geo
                            # try:
                            #     if status_content_div.find_element_by_xpath('.//span[@class="W_btn_tag"]') != []:
                            #         address= node.find_element_by_xpath('.//span[@class="W_btn_tag"]').get_attribute("title")  #geo
                            # except Exception, e:
                            #     print "Error: ", e
                            #     address=""
                            #keywords
                            try:
                                keywords = driver.find_element_by_class_name("searchInp_form").get_attribute("value").split("")  #keywords
                                keywordscom=""
                                for keyword in keywords[0:len(keywords)]:
                                    keywordscom+= keyword+"、"
                                keywordscom+= keywords[len(keywords)-1]
                                # print keywordscom
                            except Exception as e:
                                # print e.message
                                keywordscom="招商银行、招行"
                            # print keywords
                            # timestamp
                            timestamp = time.time()
                            print timestamp, comments_count, repost_count, statusurl, status_source, status_date,status_text,userurl,username
                    except Exception as e:
                        # print "Error", e.message
                             continue
                parseSuccess=True
            except Exception as e:
                continue
        if parseSuccess:
            time.sleep(random.uniform(10, 20))
            try:
                # next_page_btn = driver.find_element_by_xpath('//*[@id="pl_weibo_direct"]/div/em/em/div[1]/div/a')
                # next_page_btn.click()  # switch to next page
                next_page_link=driver.find_element_by_class_name("page next S_txt1 S_line1")
                nextpage=next_page_link.get_attribute("href")
                driver.get(nextpage)
                time.sleep(10)
                # try:
                #     search_driver.find_element_by_class_name("noresult_support")
                #     search_driver.refresh()
                #     search_driver.send_keys(Keys.ENTER)
                # except Exception, e:
                #     pass
                #
                # print "parse next page"
                self.parse_search_page(keywords, driver, urlQueue)
            except Exception, e:
                print "Error: ", e
        else:
            self.start_search(keywords,driver,urlQueue)
            print "解析页面失败"
    def parse_user_page(self, userurl,driver):  # Parse user page
        time.sleep(random.uniform(2, 8))
        # user_driver.switch_to_window(user_handle)
        # user_driver.get(userurl)
        # # write_file = open("user.json", "a")
        # while True:
        #     try:
        #         user = Users()
        #         if user_driver.current_url == "http://weibo.com/u/3344505284/home?wvr=5":
        #             break
        #         print "user info:"
        #
        #         #user name
        #         user.Name = user_driver.find_element_by_xpath('//h1[@class="username"]').text
        #
        #         #user id
        #         user.user_id = self.get_userid_using_re(
        #             user_driver.find_element_by_xpath('//div[@node-type="focusLink"]').get_attribute("action-data"))
        #
        #         #fiends count, followers count and statues count
        #         count_table = user_driver.find_element_by_xpath('//table[@class="tb_counter"]').find_elements_by_xpath(
        #             ".//td")
        #         for i, count in enumerate(count_table):
        #             count_number = count.find_element_by_xpath(".//strong").text
        #             if i == 0:
        #                 user.friends_count = count_number
        #                 print user.friends_count
        #             elif i == 1:
        #                 user.followers_count = count_number
        #                 print user.followers_count
        #             elif i == 2:
        #                 user.statuses_count = count_number
        #                 print user.statuses_count
        #             else:
        #                 pass
        #         #timestamp
        #         user.timestamp = time.time()
        #
        #         # write_file.write(json.dumps(user.tojson(), sort_keys=True, indent=4, separators=(',', ': '),skipkeys=True))
        #         # write_file.close()
        #
        #         break
        #     except Exception, e:
        #         print "Error: ", e
        #         #user_driver.send_keys(Keys.ENTER)
        #         # user_driver.refresh()
        #         try:
        #             home_page_btn = user_driver.find_element_by_xpath('//table[@class="tb_tab"]').find_element_by_xpath(
        #                 ".//a")
        #             home_page_btn.click()
        #         except Exception, e:
        #             print "Error: ", e
        #             user_driver.refresh()


    def start_search(self, keywords, driver,urlQueue):

        # 尝试搜索关键词列表

        tries_times = 0
        search_success = False
        while not search_success and tries_times <= LOGIN_MAX_TRIES / 4:
            print("start one time search ")
            tries_times += 1
            try:
                    # driver = self.comeToSearchWeiboPage(driver)
                    driver.get("http://weibo.com/")
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="plc_top"]/div/div/div[2]/input')))
                    search_input = driver.find_element_by_xpath('//*[@id="plc_top"]/div/div/div[2]/input')
                    keyword_comb = ""                #Put all keywords in a combination into a string
                    for keyword in keywords:
                        keyword_comb = keyword_comb + " " + keyword
                    search_input.send_keys(keyword_comb.decode('utf-8'))
                    search_input.send_keys(Keys.ENTER)
                    time.sleep(random.randrange(2, 3))
                    self.parse_search_page(keywords,driver, urlQueue)
                    search_success=True
            except Exception as e:
                print "Error: ", e

    def next_page(self,keywords,search_driver,urlQueue):
        try:
            time.sleep(2)
            next_page_btn = search_driver.find_element_by_xpath('//*[@id="pl_weibo_direct"]/div/em/em/div[1]/div/a')
            next_page_btn.click()  # switch to next page
            try:
                search_driver.find_element_by_class_name("noresult_support")
                time.sleep(random.uniform(3, 6))
                search_driver.refresh()
                search_driver.send_keys(Keys.ENTER)
            except Exception, e:
                pass

            print "parse next page"
            self.parse_search_page(keywords,search_driver, urlQueue)
        except Exception, e:
            print "Error: ", e


    def prepare_log_in(self, username, password, type):
        if type == "search":
            self.LoginWeibo(username, password, search_driver)
        # elif type == "user":
        # self.LoginWeibo(username, password, user_driver)
        else:
            print "Wrong log in"

    def get_userid_using_re(self, string):  # extract user id from page element
        pattern = re.compile('(?<=uid\=)[0-9]*(?=\&)')
        id = pattern.search(string)
        if id:
            id = id.group()
        print id
        return id

    def split_keyword(self, keywords):
        return keywords.split(" ")


# Initiate two Weibo instance for search page and user page

def parse_status(search_weibo, driver,urlQueue):  #thread for parsing search page
    while True:
        print("Start search Weibo!")
        # for keyword in keywords_list:
        # keywords_list    print keyword
        search_weibo.start_search(keywords_list, driver,urlQueue)
        time.sleep(random.uniform(3600, 4200))


def parse_user(user_browser,driver,urlQueue):  #thread for parsing user page
    while True:
        try:
           while len(urlQueue) > 0:
               time.sleep(random.randrange(10, 20))
               user_url=urlQueue.popleft()
               print "parseing user info ", user_url
               user_browser.parse_user_page(user_url, driver)
           time.sleep(random.randrange(1800, 2400))
        except Exception as e:
            print e.message

if __name__ == "__main__":
    user_url_que = deque()
    search_browser = Weibo()  #查找微博的浏览器
    user_browser = Weibo()    #获取微博作者信息的浏览器
    search_driver = webdriver.PhantomJS()  #Browser for search status
    user_driver = webdriver.PhantomJS()  #Browser for parsing user page

    #两个浏览器分别登录微博账号，主要为了获取cookies
    threads = []

    if search_browser.loginSinaWeibo(account_name, account_passwd, search_driver, loginURL):#完成自动登录
        search_status_thread = threading.Thread(target=parse_status, args=(search_browser, search_driver,user_url_que))   # print ("登录成功并转到微博页面")
        threads.append(search_status_thread)
    user_browser.loginSinaWeibo(account_name, account_passwd,user_driver,loginURL)

    #place parsing search page and parsing user page into two threads
    user_info_thread = threading.Thread(target=parse_user, args=(user_browser, user_driver, user_url_que))
    threads.append(user_info_thread)

    for thread in threads:
        thread.start()
    #
    # #主线程等待子线程结束后退出，虽然子线程死了才要退
    for thread in threads:
        thread.join()
