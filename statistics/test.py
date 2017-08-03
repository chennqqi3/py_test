# coding=utf-8
import os
import base
import behavior
import freq
import retention
import pvuv
import urllib2
from datetime import date
from timeit import Timer
import doctest
import bisect


def tt():
    print 'dddd'
    return 12


if __name__ == '__main__':

    path = 'd:\\log\\'
    activate_file_list = []
    stat_file_list = []
    register_file_list = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            if f[0:13] == 'activate.log.':
                activate_file_list.append(f)
            if f[0:9] == 'stat.log.':
                stat_file_list.append(f)
            if f[0:13] == 'register.log.':
                register_file_list.append(f)

    stat_file_list.append('stat.log')
    activate_file_list.append('activate.log')
    register_file_list.append('register.log')

    base.base(path, activate_file_list, stat_file_list, register_file_list)
    behavior.behavior()
    freq.freq(path, stat_file_list)
    retention.retention(path, stat_file_list)
    pvuv.pvuv(path, stat_file_list)
    for line in urllib2.urlopen("http://www.rongcloud.cn/"):
        line = line.decode('utf-8')
        # print line
