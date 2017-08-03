#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run mysql_by_day'
    try:
        flag = os.system('/home/capvision/script/mysql_by_day.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.95 mysql_by_day ",
                              '192.168.50.95 run mysql_by_day error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.95 mysql_by_day ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
