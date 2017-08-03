# coding=utf-8
import re
import gzip
import os

path = "/usr/local/nginx/logs/"

dic = []


def main(pth):
    # pth = "ndb.access.log-20160228.gz"
    with gzip.open(path + pth) as file_object:
        for line in file_object:
            line = line.strip()
            if line.find("http://db.capvision.com/client") != -1:
                # print line
                tmp = re.findall(r'http://db.capvision.com/client.*?"', line)
                if tmp[0].find("?") != -1:
                    tmp = re.findall(r'http://db.capvision.com/client.*?\?', tmp[0])
                    tmp[0] = tmp[0].replace("?", "")
                if tmp[0] in dic:
                    pass
                else:
                    dic.append(tmp[0].replace("?", ""))

    return dic


if __name__ == '__main__':
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            if f.find("ndb.access.log") != -1 and f.find(".gz") != -1:
                main(f)
    print dic, len(dic)
