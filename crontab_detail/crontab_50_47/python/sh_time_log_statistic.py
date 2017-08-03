#!/usr/bin/python
# coding=utf-8
import time
import os
from monitor import monitor
import datetime


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run monitor time_log_statistic log'
    try:
        flag = os.system('/usr/bin/python /opt/code/py_helper/monitor/time_log_statistic.py')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ",
                              '192.168.50.47 run monitor time_log_statistic log error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
