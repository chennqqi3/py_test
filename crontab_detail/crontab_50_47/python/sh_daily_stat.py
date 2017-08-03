#!/usr/bin/python
# coding=utf-8

from statistics import stat
from monitor import monitor


def main():
    try:
        stat.main()
    except Exception, e:
        monitor.send_mail(monitor.mail_to_list, "192.168.50.47 python ", e)

main()
