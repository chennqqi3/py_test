import os
import re


def calc(month):
    # path = "/data/logs/ks_web"
    path = "c:"
    pv_dic = []
    stat_files = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            if f[0:15] == 'log.log.' + month:
                stat_files.append(f)
    for f in stat_files:
        with open(path + f) as pf:
            for line in pf:
                # all_data = line.split("postData: ")
                # tmp_arr = eval(all_data[1])
                # uid = tmp_arr["uid"]
                # if uid not in pv_dic:
                #     pv_dic.append(uid)
                regex = ur".*postData.*"
                match = re.search(regex, line)
                if match:
                    try:
                        all_data = match.group().split("postData: ")
                        tmp_arr = eval(all_data[1])
                        mobile = tmp_arr["userid"]
                        if mobile not in pv_dic:
                            pv_dic.append(mobile)
                    except Exception , e:
                        continue
                        # print "error", line


    print month, len(pv_dic)

if __name__ == '__main__':
    # calc("2016-01")
    calc("2016-02")
    # calc("2016-03")
    # calc("2016-04")
    # calc("2016-05")
    # calc("2016-06")