# coding=utf-8

import time
import re
import os
import sys
import codecs
import shutil
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def LoginWeibo(username,password):
    try:
        driver.get("https://passport.weibo.cn/signin/login")
        elem_user = driver.find_element_by_id("loginName")
        time.sleep(5)
        elem_user.send_keys(username)

        elem_pwd = driver.find_element_by_id("loginPassword")
        time.sleep(5)
        elem_pwd.send_keys(password)

        time.sleep(5)

        elem_sub = driver.find_element_by_id("loginAction")
        elem_sub.click()
        time.sleep(2)

        #print driver.current_url
        #print driver.get_cookies()  #获得cookie信息 dict存储
        #print u'输出Cookie键值对信息:'
        #for cookie in driver.get_cookies():
            #print cookie
        #    for key in cookie:
        #        print key, cookie[key]

        print "succesfully log in"
    except Exception,e:
        print "Error: ",e

def VisitPersonPage(user_id,pages):
    try:
        driver.get("http://weibo.cn/"+user_id)

        print u'个人详细信息'
        print '****************************************************************'
        print u'用户id: ' + user_id

        str_name = driver.find_element_by_xpath("//div[@class='ut']")
        arr = str_name.text.split(" ")
        name = arr[0]
        print u'用户名称：' + name

        str_wb = driver.find_element_by_xpath("//div[@class='tip2']")
        # ??
        pattern = r"\d+\.?\d*"

        guid = re.findall(pattern,str_wb.text,re.S|re.M)
        for value in guid:
            num_wb = int(value)
            print u'微博数：'+str(num_wb)
            break

        str_gz = driver.find_element_by_xpath("//div[@class='tip2']/a[1]")
        guid = re.findall(pattern, str_gz.text, re.M)
        num_gz = int(guid[0])
        print u'关注数: ' + str(num_gz)

        str_fs = driver.find_element_by_xpath("//div[@class='tip2']/a[2]")
        guid = re.findall(pattern, str_fs.text, re.M)
        num_fs = int(guid[0])
        print u'粉丝数: ' + str(num_fs)

        # write to file
        #***********************************************************************
        #
        #***********************************************************************

        # get weibo content
        page = 1
        allPages = pages
        base_url = "http://weibo.cn/"
        while page <= allPages:
            url = base_url + user_id + "?page=" + str(page)
            driver.get(url)
            allInfo = driver.find_elements_by_xpath("//div[@class='c']")

            for value in allInfo:
                info = value.text

                if u'设置' not in info and u'彩版' not in info:
                    if(info.startswith(u'转发')):
                        print u'转发微博'
                    else:
                        print u'原创微博'

                    str1 = info.split(u'赞')[-1]
                    if str1:
                        val1 = re.findall("\d+",str1)
                        if len(val1) != 0:
                            print u'点赞数：'+val1[0]

                    str2 = info.split(u'转发')[-1]
                    if str2:
                        val2= re.findall("\d+",str2)
                        if len(val2) != 0:
                            print u'转发数：'+val2[0]

                    str3 = info.split(u'评论')[-1]
                    if str3:
                        val3 = re.findall("\d+",str3)
                        if len(val3) != 0:
                            print u'评论数：'+val3[0]

                    str4 = info.split(u'收藏')[-1]
                    flag = str4.find(u'来自')
                    print u'时间: ' + str4[:flag]

                    print u'微博内容:'
                    print info[:info.rindex(u'赞')]

            page += 1

    except Exception,e:
        print "Error: ",e


if __name__ == '__main__':
    driver = webdriver.Firefox()
    wait = ui.WebDriverWait(driver,18)

    LoginWeibo("*******","*******")
    VisitPersonPage("weibo url",5)
