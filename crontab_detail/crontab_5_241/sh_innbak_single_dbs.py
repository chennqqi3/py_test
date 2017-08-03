#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run innbak_single_dbs'
    try:
        flag = os.system('/home/capvision/script/innbak_single_dbs.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.5.241 innbak_single_dbs ",
                              '192.168.5.241 run innbak_single_dbs error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.5.241 innbak_single_dbs ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
