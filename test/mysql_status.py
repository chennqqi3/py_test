#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
from monitor import monitor


def main():
    # command = 'mysql -uadmin_sup -padmin_sup4096  --socket=/data/mysql_16/mysql.sock -e "show slave status \G" '
    command = 'ping www.baidu.com '
    r = os.popen(command)
    info = r.readlines()
    for line in info:
        line = line.strip('\r\n')
        if line.find("Seconds_Behind_Master") != -1:
            arr = line.split(':')
            if len(arr) > 1:
                status = arr[1].replace(' ', '')
                if status.isdigit():
                    print arr[1]
                else:
                    monitor.send_mail(monitor.mail_to_list, '5.241 mysql Master-slave relationship was disconnected',
                                      '5.241 mysql Master-slave relationship was disconnected')

if __name__ == '__main__':
    main()
    monitor.send_mail(monitor.mail_to_list, '5.241 mysql Master-slave relationship was disconnected',
                      '5.241 mysql Master-slave relationship was disconnected')