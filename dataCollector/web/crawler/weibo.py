# -*- coding: utf-8 -*-
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

user_url_que = deque()
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
                driver.get(loginUrl)
                elem_user = driver.find_element(by=By.ID, value="username")  #登录 用户名输入框
                elem_user.send_keys(username)  #fill in username
                elem_pwd = driver.find_element(by=By.ID, value="password")  #登录密码框
                elem_pwd.send_keys(password)  #fill in password
                elem_sub = driver.find_element_by_xpath('//input[@type="submit"]')
                time.sleep(1)
                elem_sub.click()  #click login button
                time.sleep(5)
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
            return self.comeToSearchWeiboPage(driver)  #登录成功

    def comeToSearchWeiboPage(self, driver):
        """
        :param driver: 浏览器
        :return:
        """
        switch_page_success = False
        try_times = 0
        while not switch_page_success and try_times <= LOGIN_MAX_TRIES / 2:
            try:
                try_times += 1
                time.sleep(3)
                weibo_link = driver.find_element_by_link_text(u"我的微博")
                print weibo_link.get_attribute("href")

                weiboHomePage = weibo_link.get_attribute("href")  # http://weibo.com/
                # print weiboHomePage
                driver.get(weiboHomePage)
                switch_page_success = True
            except Exception as e:
                print("Error!:" + e.message)
                if try_times <= LOGIN_MAX_TRIES / 2:
                    continue
                else:
                    return False
        if try_times > LOGIN_MAX_TRIES / 2:
            return False
        else:
            return switch_page_success

    def parse_search_page(self, driver):


        print "parse one page"
        try:
            # results = driver.find_elements_by_class_name("WB_cardwrap S_bg2 clearfix")
            time.sleep(10)
            # results = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located_located((By.XPATH, '//div[@class="WB_cardwrap S_bg2 clearfix"]')))
            results = driver.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]')
            print len(results)
            print results
            for node in results:
                try:
                    status_content_div = node.find_element_by_xpath('.//div[@action-type="feed_list_item"]')

                    if status_content_div != []:
                        status_id = status_content_div.get_attribute("mid")  # id #status id
                        print status_id
                        user_simple = {}  # 微博作者简要信息
                        user_link_info = status_content_div.find_element_by_xpath('.//a[@class="W_texta W_fb"]')
                        if user_link_info != []:
                            print user_link_info.text
                            user_simple["name"] = user_link_info.text.strip()
                            print user_link_info.get_attribute("href")
                except Exception as e:
                    print "Error", e.message
                    # except Exception as e:
                    # print "Error:","has no status content",e.message
                    #
                    #
                    #
                    #
                    #
                    #     #user simple and user url
                    #     if node.find_element_by_xpath('.//a[@class="W_texta W_fb"]') != []:
                    #         self.status.user_simple["name"] = (
                    #         node.find_element_by_xpath('.//a[@class="W_texta W_fb"]')).text.replace(" ", "")  #username
                    #         self.status.userurl = node.find_element_by_xpath('.//a[@class="W_texta W_fb"]').get_attribute(
                    #             "href")  #userurl
                    #         # self.parse_user_page(self.status.userurl)
                    #         global user_url_que
                    #         if self.status.userurl not in user_url_que:
                    #             user_url_que.append(self.status.userurl)
                    #         print self.status.user_simple["name"]
                    #         print self.status.userurl
                    #
                    #     #comment text
                    #     if node.find_element_by_xpath('.//p[@class="comment_txt"]') != []:
                    #         self.status.text = node.find_element_by_xpath('.//p[@class="comment_txt"]').text  #text
                    #         print self.status.text
                    #
                    #     #date and status url
                    #     if node.find_element_by_xpath('.//a[@node-type="feed_list_item_date"]') != []:
                    #         self.status.date = node.find_element_by_xpath(
                    #             './/a[@node-type="feed_list_item_date"]').get_attribute("title")  #date
                    #         self.status.statusurl = node.find_element_by_xpath(
                    #             './/a[@node-type="feed_list_item_date"]').get_attribute("href")  #statusurl
                    #         print self.status.date
                    #         print self.status.statusurl
                    #
                    #     #source
                    #     if node.find_element_by_xpath('.//a[@rel="nofollow"]') != []:
                    #         self.status.source = node.find_element_by_xpath('.//a[@rel="nofollow"]').get_attribute(
                    #             "text")  #source
                    #         print self.status.source
                    #
                    #     #repost count
                    #     try:
                    #         repost_count = node.find_element_by_xpath(
                    #             './/a[@action-type="feed_list_forward"]').find_element_by_xpath('.//em').text
                    #         if repost_count != "":
                    #             self.status.repost_count = repost_count
                    #         else:
                    #             self.status.repost_count = 0
                    #     except:
                    #         self.status.repost_count = 0
                    #     print self.status.repost_count
                    #
                    #     #comments count
                    #     try:
                    #         # if node.find_element_by_xpath('.//a[@action-type="feed_list_comment"]').find_element_by_xpath('.//em') != []:
                    #         comments_count = node.find_element_by_xpath(
                    #             './/a[@action-type="feed_list_comment"]').find_element_by_xpath('.//em').text
                    #         if comments_count != "":
                    #             self.status.comments_count = comments_count
                    #         else:
                    #             self.status.comments_count = 0
                    #     except Exception, e:
                    #         print "Error: ", e
                    #         self.status.comments_count = 0
                    #     print self.status.comments_count
                    #
                    #     #attitude count
                    #     try:
                    #         attitude_count = node.find_element_by_xpath(
                    #             './/a[@action-type="feed_list_like"]').find_element_by_xpath('.//em').text
                    #         if attitude_count != "":
                    #             self.status.attitude_count = attitude_count
                    #         else:
                    #             self.status.attitude_count = 0
                    #     except Exception, e:
                    #         print "Error: ", e
                    #         self.status.attitude_count = 0
                    #     print self.status.attitude_count
                    #
                    #     # if node.find_element_by_xpath('.//a[@class="W_textb"]') != []:
                    #     #     self.status.statusurl = node.find_element_by_xpath('.//a[@class="W_textb"]').get_attribute("href")#statusurl
                    #
                    #     #geo
                    #     try:
                    #         if node.find_element_by_xpath('.//span[@class="W_btn_tag"]') != []:
                    #             self.status.geo["address"] = node.find_element_by_xpath(
                    #                 './/span[@class="W_btn_tag"]').get_attribute("title")  #geo
                    #     except Exception, e:
                    #         print "Error: ", e
                    #         self.status.geo = {}
                    #
                    #     #keywords
                    #     self.status.keywords = search_driver.find_element_by_class_name("searchInp_form").get_attribute(
                    #         "value").split(" ")  #keywords
                    #
                    #     try:
                    #         self.status.pic_urls = []
                    #         pic_results = node.find_elements_by_xpath('.//img[@class="bigcursor"]')
                    #         for pic in pic_results:
                    #             self.status.pic_urls.append(pic.get_attribute("src").encode("utf-8"))
                    #     except Exception, e:
                    #         print "Error: ", e
                    #
                    #     #timestamp
                    #     self.status.timestamp = time.time()
        except Exception as e:
            print "Error", e.message
            # Parse search result page in a for loop
            # write_file.write(json.dumps(self.status.tojson(), sort_keys=True, indent=4, separators=(',', ': '),skipkeys=True))
        # wait 20 ~ 40 seconds to pare next page
        time.sleep(random.uniform(20, 40))
        # self.next_page()

    def parse_user_page(self, userurl):  # Parse user page
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


    def start_search(self, keywords, driver):

        # 尝试搜索关键词列表

        tries_times = 0
        search_success = False
        while not search_success and tries_times <= LOGIN_MAX_TRIES / 4:
            print("start one time search ")
            tries_times += 1
            try:
                # driver.get()
                time.sleep(random.randrange(4, 5))
                # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gn_search_v2")))
                search_area = driver.find_element_by_class_name('gn_search_v2')
                search_input = search_area.find_element_by_xpath('.//input[@node-type="searchInput"]')
                #Put all keywords in a combination into a string
                keyword_comb = ""
                for keyword in keywords:
                    keyword_comb = keyword_comb + " " + keyword
                search_input.send_keys(keyword_comb.decode('utf-8'))
                search_input.send_keys(Keys.ENTER)
                search_btn = search_area.find_element_by_xpath('.//a[@node-type="searchSubmit"]')
                search_btn.click()

                time.sleep(3)
                self.parse_search_page(driver)
                # list_count = len(driver.find_element_by_xpath('//div[@class="layer_menu_list W_scroll"]')\
                #                      .find_elements_by_xpath(".//li"))
                # more_result_btn = search_driver.find_element_by_xpath('//div[@class="search_rese clearfix"]') \
                #         .find_element_by_xpath(".//a")
                # if list_count <= 30 and more_result_btn:
                #         print "click more result button"
                #         more_result_btn.click()
                #         time.sleep(random.uniform(1, 3))
                # self.parse_search_page()
                break
            except Exception as e:
                print "Error: ", e

    def next_page(self):
        try:
            time.sleep(2)
            next_page_btn = search_driver.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]')
            next_page_btn.click()  # switch to next page

            try:
                search_driver.find_element_by_class_name("noresult_support")
                time.sleep(random.uniform(3, 6))
                search_driver.refresh()
                # search_driver.send_keys(Keys.ENTER)
            except Exception, e:
                pass

            print "parse next page"
            self.parse_search_page()
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

def parse_status(search_weibo, driver):  #thread for parsing search page
    while True:
        print("Start search Weibo!")
        # for keyword in keywords_list:
        # keywords_list    print keyword
        search_weibo.start_search(keywords_list, driver)
        time.sleep(random.uniform(3600, 4200))


def parse_user(driver):  #thread for parsing user page
    print "start user thread"
    while True:
        time.sleep(random.uniform(10, 30))
        try:
            while user_url_que:
                user_url = user_url_que.popleft()
                print "Try to parse" + user_url
                user_weibo.parse_user_page(user_url)
        except:
            pass


if __name__ == "__main__":

    search_browser = Weibo()  #查找微博的浏览器
    # user_browser = Weibo()    #获取微博作者信息的浏览器

    search_driver = webdriver.Firefox()  #Browser for search status
    wait = ui.WebDriverWait(search_driver, 10)

    # user_driver = webdriver.Firefox()  #Browser for parsing user page
    # wait = ui.WebDriverWait(user_driver, 10)


    #两个浏览器分别登录微博账号，主要为了获取cookies

    random.shuffle(keywords_list)  #disorder the list of keywords

    threads = []
    #完成自动登录
    if search_browser.loginSinaWeibo(account_name, account_passwd, search_driver, loginURL):
        # print ("登录成功并转到微博页面")
        search_status_thread = threading.Thread(target=parse_status, args=(search_browser, search_driver))
        threads.append(search_status_thread)

    # user_browser.loginSinaWeibo(account_name, account_passwd,user_driver,loginURL)



    #place parsing search page and parsing user page into two threads





    # user_info_thread = threading.Thread(target=parse_user, args=(user_driver,))
    # threads.append(user_info_thread)

    for thread in threads:
        thread.start()
    #
    # #主线程等待子线程结束后退出，虽然子线程死了才要退
    for thread in threads:
        thread.join()
