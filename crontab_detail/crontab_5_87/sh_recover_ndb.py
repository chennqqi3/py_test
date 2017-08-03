#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor

mail_to_list = ['dhu@capvision.com']


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run recover_ndb'
    try:
        flag = os.system('/home/capvision/reco_new.sh')
        if flag != 0:
            monitor.send_mail(mail_to_list, "192.168.5.87 recover_ndb ",
                              '192.168.5.87 run recover_ndb error')
    except Exception, e:
        monitor.send_mail(mail_to_list, "192.168.5.87 recover_ndb ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
