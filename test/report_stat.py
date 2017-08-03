import os
import gzip
import re

if __name__ == '__main__':
    path = "/home/networklog/"
    pv_dic = []
    stat_dic = {}
    stat_files = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            if f[0:21] == 'ndb.access.log-201605':
                stat_files.append(f)
    for f in stat_files:
        with gzip.open(path + f) as pf:
            for line in pf:
                if line.find("GET /report/") != -1:
                    regex = ur"GET /report/.*?/"
                    match = re.search(regex, line)
                    if match:
                        match_str = match.group()
                        key = match_str.replace("GET /report/", "").replace("/", "")
                        stat_dic.setdefault(key, 0)
                        stat_dic[key] += 1
                if line.find("GET /pn/app/report/") != -1 and line.find("\.js") == -1 and line.find(
                        "\.css") == -1 and line.find("\.jpg") == -1 and line.find("\.png") == -1:
                    regex = ur"GET /pn/app/report/.*?/"
                    match = re.search(regex, line)
                    if match:
                        match_str = match.group()
                        key = match_str.replace("GET /pn/app/report/", "").replace("/", "")
                        stat_dic.setdefault(key, 0)
                        stat_dic[key] += 1

    pv_dic = sorted(stat_dic.iteritems(), key=lambda d: d[1], reverse=True)
    print pv_dic

    stat_dic = {}
    ip_dic = {}
    for f in stat_files:
        with gzip.open("c:\\ndb.access.log_201604m.gz") as pf:
            for line in pf:
                if line.find("GET /report/") != -1:
                    regex = ur"GET /report/.*?/"
                    match = re.search(regex, line)
                    if match:
                        ip = line.split(" ")[0]
                        match_str = match.group()
                        key = match_str.replace("GET /report/", "").replace("/", "")
                        stat_dic.setdefault(key, 0)
                        stat_dic[key] += 1
                        ip_dic.setdefault(key, "")
                        if ip_dic[key].find(ip) == -1:
                            ip_dic[key] += "," + ip
                if line.find("GET /pn/app/report/") != -1 and line.find("\.js") == -1 and line.find(
                        "\.css") == -1 and line.find("\.jpg") == -1 and line.find("\.png") == -1:
                    regex = ur"GET /pn/app/report/.*?/"
                    match = re.search(regex, line)
                    if match:
                        ip = line.split(" ")[0]
                        match_str = match.group()
                        key = match_str.replace("GET /pn/app/report/", "").replace("/", "")
                        stat_dic.setdefault(key, 0)
                        stat_dic[key] += 1
                        ip_dic.setdefault(key, "")
                        if ip_dic[key].find(ip) == -1:
                            ip_dic[key] += "," + ip
    uv_stat = {}
    uv_dic = []
    for key, value in ip_dic.items():
        if value != '':
            value = value[1: len(value)]
        uv_stat.setdefault(key, 0)
        uv_stat[key] = len(value.split(","))

    uv_dic = sorted(uv_stat.iteritems(), key=lambda d: d[1], reverse=True)
    print uv_dic
