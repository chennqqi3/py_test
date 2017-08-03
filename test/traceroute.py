# coding=utf-8

import os
import datetime
import time
import threading
import sched

from decorator import new_thread
from apscheduler import schedulers

dic = {}


@new_thread
def ping_ip(dic):
    while 1:
        for ip,place in dic.items():
            result = os.system('ping  ' + ip)
            flag = 'true'
            if result == 1:
                flag = 'false'
            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            with open('ip_status.txt', 'a') as file_object:
                file_object.write('\n' + otherStyleTime + ' ping '+ place+'  '+ip+ '  ' + flag)
            time.sleep(5)


dic = {'192.168.50.1':'','192.168.50.185':'','192.168.50.47':'','101.231.189.126': '上海office_电信',
       '210.13.65.98': '上海office_联通', '106.2.219.122': 'beijing_office', '58.210.18.18': 'suzhou_office',
       '103.24.116.50': 'idc_emergency', '122.144.166.146': 'idc_fanghuoqaing', '122.144.166.147': 'idc_webs',
       '122.144.166.148': 'idc_webs', '122.144.166.149': 'idc_webs', '122.144.166.150': 'idc_webs',
       '210.13.65.97': 'shanghai_off_liantong_gateway', '101.231.189.125': 'shanghai_off_dianxin_gateway',
       '192.168.253.1': 'shanghai_off_hongkong_gateway', '192.168.5.19': '', '10.0.1.12': 'voip_nuoqing_idc'}


schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    #    os.system(cmd)
    print(time.time())
    print(' write to base',time.time() -tt)
    global tt
    tt=time.time()


def timming_exe(cmd, inc = 60):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    #  # 持续运行，直到计划时间队列变成空为止
    schedule.run()

if __name__ == '__main__':
    tt = time.time()
    print("show time after 5 seconds:",tt)
    timming_exe("echo %time%", 5)