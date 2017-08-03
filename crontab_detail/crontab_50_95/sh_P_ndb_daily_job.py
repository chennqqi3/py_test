#!/usr/bin/python
# coding=utf-8
import datetime
import os
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run P_ndb_daily_job'
    try:
        flag = os.system('/usr/local/mysql/bin/mysql -ucronjob -p123456 -e"call ndb.P_ndb_daily_job()";')
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.95 P_ndb_daily_job ",
                              '192.168.50.95 run P_ndb_daily_job error')
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.95 P_ndb_daily_job ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')


main()
