#!/usr/bin/python
# coding=utf-8
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')


def url_get(url,title):
    print title,url
    driver.get(url)


def get_following(spectext):
    #billnotes_link = driver.find_element_by_css_selector('.span12 .unit .unit-content .row-fluid .span9').text
    ele =  driver.find_element_by_xpath("//div[contains(text(), '%s')]/following-sibling::*[1]"%spectext)
    return ele


def read_assertval():
    hours_link= get_following('Client Hour').text
    billnotes_link = get_following('Billing Notes')
    lines_num = len(billnotes_link.text.split('\n'))
    return hours_link,lines_num


def change_indiag(hours,billnotes):
    driver.find_element_by_id('hours').clear()

    billnotes = 'asdfasf234'
    driver.find_element_by_id('hours').send_keys(str(hours))
    driver.find_element_by_id('billnotes').clear()
    driver.find_element_by_id('billnotes').send_keys(billnotes)
    button = driver.find_element_by_xpath("//div[@id='change_client-view']/following-sibling::*[1]/div/button[1]")
    button.click()


def change_clienthour(proj_id):
    url_get( 'http://tys.ndb.capvision.com/project/consultation/index/tasklist?id=%d'%proj_id,'tasklist')
    task_id =  driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]/div/a").text
    url_get('http://tys.ndb.capvision.com/project/consultation/index/viewtask?taskid=%s'%task_id, 'view task')
    hours,billnotes = 9,'asdfsaf23'
    hours_link,lines_num_old = read_assertval()
    driver.find_element_by_id('client_hour_link').click()
    time.sleep(2)
    change_indiag(hours,billnotes)
    time.sleep(5)
    hours_link,lines_num_new = read_assertval()
    if int(float(hours_link)) == hours and lines_num_new == lines_num_old+1 : print 'change saved okay, now lines= %d '%lines_num_new


def change_consultant_hour(proj_id):

    task_id = 277350
    url ='http://tys.ndb.capvision.com/project/consultation/index/viewtask?taskid=%d'%task_id
    driver.get(url)


    #consultant_minutes = get_following('Consultant minutes')
    #payment_notes = get_following('Payment Notes')
    #lines_num_old = len(payment_notes.text.split('\n'))
    #print     payment_notes.text,
    #print lines_num_old
    #return

    driver.switch_to_window(driver.window_handles[-1])
    driver.find_element_by_id('consultant_hour_id').click()
    time.sleep(3)


    driver.find_element_by_id('consultant_hours').clear()
    hours = 1
    #billnotes = 'tys1234'
    #driver.find_element_by_id('consultant_hours').send_keys(str(hours))
    driver.find_element_by_id('cash').clear()
    driver.find_element_by_id('cash').send_keys('12')
    driver.find_element_by_id('paymentnotes').clear()
    driver.find_element_by_id('paymentnotes').send_keys('tys1234')
    driver.implicitly_wait(3)
    button = driver.find_element_by_xpath("//div[@id='change_consultant-view']/following-sibling::*[1]/div/button[1]")
    print button.get_attribute("class")
    button.click()
    time.sleep(3)
    return

    print button.get_attribute("class")
    if button.is_displayed():
        print 'button clicked'
        button.click()

    button.click()
    time.sleep(3)
    consultant_minutes = get_following('Consultant Minutes').text
    payment_notes =  get_following('Payment Notes')
    lines_num_new = len(payment_notes.text.split('\n'))
    #print     billnotes_link.text,
    #print lines_num_old

    if int(float(consultant_minutes)) == hours*60 and lines_num_new == lines_num_old+1 : print 'change saved okay, now lines= %d '%lines_num_new



def clienthour(proj_id):
    if check_complete(proj_id) == 'Complete':
        change_clienthour(proj_id)

# def proj_casecode(proj_id):

def consultant_info(proj_id):
    if check_complete(proj_id) == 'Complete':
        change_consultant_hour(proj_id)

def check_complete(proj_id):
    url='http://tys.ndb.capvision.com/project/consultation/index/view?id=%d'%proj_id
    url_get(url,'proj_consultation view')
    #driver.maximize_window()
    time.sleep(5)
    proj_status = driver.find_element_by_id('project_status').text
    print 'url %s project status proj_id %d %s'%(url,proj_id,proj_status)
    return proj_status



def login():
    driver.get('http://tys.ndb.capvision.com/')
    driver.maximize_window()
    driver.find_element_by_id('LoginForm_username').send_keys('admin')
    driver.find_element_by_id('LoginForm_password').send_keys('123456')
    driver.find_element_by_name('yt0').click()
    time.sleep(1)

login()
clienthour(6260)
# proj_casecode(6260)
consultant_info(6348)