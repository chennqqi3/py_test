#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run monitor log'
    try:
        flag = os.system('sh /opt/code/py_helper/run_monitor_log.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ", '192.168.50.47 run monitor log error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')

main()
