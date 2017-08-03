#!/usr/bin/python
# coding=utf-8

import os
import datetime
from monitor import monitor


def main():
    today_time = datetime.datetime.now()
    print 'begin: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')
    print 'run update consultant special tag'
    try:
        flag = os.system("/usr/local/php/bin/php /home/www/ndb/protected/yiic consultant updateConsultantSpecialTag")
        if flag != 0:
            monitor.send_mail(monitor.mail_to_list, "192.168.50.47 php ",
                              "192.168.50.47 php run update consultant special tag fail")
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.47 php ", e)
    today_time = datetime.datetime.now()
    print 'end: ', datetime.datetime.strftime(today_time, '%Y-%m-%d %H:%M:%S')

main()
