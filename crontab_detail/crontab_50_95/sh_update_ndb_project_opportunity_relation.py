#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run update_ndb_project_opportunity_relation'
    try:
        flag = os.system('/usr/bin/python /home/capvision/script/update_ndb_project_opportunity_relation.py')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.95 update_ndb_project_opportunity_relation ",
                              '192.168.50.95 run update_ndb_project_opportunity_relation error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.95 update_ndb_project_opportunity_relation ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
