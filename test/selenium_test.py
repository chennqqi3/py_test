#!/usr/bin/python
# coding=utf-8

from selenium import webdriver
# 引入ActionChains鼠标操作类
from selenium.webdriver.common.action_chains import ActionChains
# 引入keys类操作
from selenium.webdriver.common.keys import Keys
import time


def s(int):
    time.sleep(int)
# browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
browser = webdriver.Firefox()
browser.get('http://www.hao123.com/')
print u'现在将浏览器最大化'
browser.maximize_window()

print browser.current_window_handle
browser.find_element_by_link_text(u"百度").click()
browser.close()
browser.switch_to_window(browser.window_handles[-1])

browser.find_element_by_link_text(u"登录").click()

browser.switch_to_window(browser.window_handles[-1])

browser.find_element_by_id('TANGRAM__PSP_8__userName').send_keys('karolong')
browser.find_element_by_id('TANGRAM__PSP_8__password').send_keys('396500636')
browser.find_element_by_id('TANGRAM__PSP_8__submit').click()

browser.switch_to_window(browser.window_handles[-1])
browser.find_element_by_id('TANGRAM__PSP_30__closeBtn').click()
browser.find_element_by_name('tj_trtieba').click()
browser.close()

browser.switch_to_window(browser.window_handles[-1])
# print browser.current_url
# browser.find_element_by_link_text("百度首页").click()
# browser.switch_to_window(browser.window_handles[0])
# print browser.current_url
time.sleep(3)

browser.quit()


