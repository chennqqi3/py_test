# coding=utf-8
import os

import base
import behavior
import freq
import retention
import pvuv
import article_report


def main():
    path = 'c://'

    if not os.path.isdir(path):
        print 'no stat'
        return

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
    # activate_file_list.append('activate.log')
    # register_file_list.append('register.log')

    # base.base(path, activate_file_list, stat_file_list, register_file_list)
    # freq.freq(path, stat_file_list)
    retention.retention(path, stat_file_list)
    # pvuv.pvuv(path, stat_file_list)
    # article_report.main()
    # behavior.behavior()


if __name__ == '__main__':
    main()
