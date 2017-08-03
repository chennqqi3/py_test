import sys
import os
import re
import urllib
import subprocess
import time


# def getlocation(ip):
#     result = urllib.urlopen(ip)
#     res = result.readlines()
#     print res
#     result.close()
#     for i in res:
#         if re.match(".*ul class=\"ul1\".*",i):
#             ipblock=i
#     if 'ipblock' in dir():
#         add1 = ipblock.split("<")[3].split(">")[1].decode('gb2312')[6:].encode('utf8')
#         add2 = ipblock.split("<")[5].split(">")[1].decode('gb2312')[6:].encode('utf8')
#         if add1 == add2:
#             return "\t\t\t"+add1
#         else:
#             return "\t\t\t"+add1+"\tOR\t"+add2

# if len(sys.argv) < 2:
#     print "Usage: %s {hostname|ip}" % sys.argv[0]
#     sys.exit()
# else:
#     host = sys.argv[1]

# try:
#     p = subprocess.Popen(['/bin/traceroute',host],stdout=subprocess.PIPE)
#     while True:
#         line = p.stdout.readline()
#         if not line:
#             break
#         if re.match("^.[0-9].*(.*).*",line):
#             try:
#                 ip = line.split('(')[1].split(')')[0]
#                 print line+getlocation(ip)
#             except IndexError,e:
#                 print line,
#         else:
#             print line,
# except (KeyboardInterrupt,SystemExit):
#     sys.exit()

def hel(t):
    return os.system('tracert www.baidu.com')

if __name__ == '__main__':
    i = 0
    # file_object = 'd:\\test.txt'
    while i < 3:
        print hel('t')
        # cmd = 'cmd.exe /k ping www.baidu.com'
        # os.system('cmd.exe /k ping www.baidu.com')
        # file_object = open('d:\\test.txt', 'w')
        # file_object.close()
        # os.system('tracert www.baidu.com')
        subprocess.Popen('tracert www.baidu.com')
        time.sleep(5)
        i += 1
