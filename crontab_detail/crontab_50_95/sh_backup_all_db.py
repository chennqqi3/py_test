#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run backup_all_db'
    try:
        flag = os.system('/home/capvision/script/backup_all_db.sh')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.95 backup_all_db ",
                              '192.168.50.95 run backup_all_db error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.95 backup_all_db ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
