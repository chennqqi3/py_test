#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run mysql_by_nmin'
    try:
        flag = os.system('/home/capvision/script/mysql_by_nmin.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.95 mysql_by_nmin ",
                              '192.168.50.95 run mysql_by_nmin error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.95 mysql_by_nmin ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
