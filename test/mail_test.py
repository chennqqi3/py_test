#!/usr/bin/python
# coding=utf-8
from monitor import monitor

if __name__ == '__main__':
    monitor.send_mail(monitor.mail_to_list, 'from python mail', 'python send mail')
