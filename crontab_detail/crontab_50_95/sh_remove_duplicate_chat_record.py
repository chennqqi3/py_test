#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run remove_duplicate_chat_record'
    try:
        flag = os.system('/home/capvision/script/remove_duplicate_chat_record.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.95 remove_duplicate_chat_record ",
                              '192.168.50.95 run remove_duplicate_chat_record error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.95 remove_duplicate_chat_record ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
