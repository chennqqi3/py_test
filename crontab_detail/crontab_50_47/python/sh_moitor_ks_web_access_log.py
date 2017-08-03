#!/usr/bin/python
# coding=utf-8
import time
import os
from monitor import monitor
import datetime


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run monitor ks_web_access log'
    try:
        flag = os.system('sh /opt/code/py_helper/run_moitor_ks_web_access_log.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ",
                              '192.168.50.47 run monitor ks_web_access log error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
