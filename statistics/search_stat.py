# coding=utf-8

import os
import time
import json


def sort_dic(dic):
    darr = sorted(dic.items(), key=lambda d: d[1])
    return darr


def main():
    # path = '/data/logs/ks_stat/'
    path = 'c:\\'

    if not os.path.isdir(path):
        print 'no stat'
        return

    stat_file_list = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f):
            if f[0:8] == 'log.log.':
                stat_file_list.append(f)

    stat_file_list.append('log.log')

    city_map = {}
    city_industry_map = {}
    query_map = {}
    industry_map = {}

    object_txt = open('d:\\search.txt', 'a')

    for pth in stat_file_list:
        stat_day = pth.replace('log', '').replace('.', '')
        if stat_day == '':
            stat_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print stat_day

        city_day_map = {}
        city_day_industry_map = {}
        query_day_map = {}
        industry_day_map = {}

        with open(path + pth) as file_object:
            flag = 20
            for line in file_object:
                line = line.strip()
                flag += 1
                if line.find("ks_web/api/search") != -1:
                    flag = 0
                if flag == 1:
                    tmp_arr = line.split(" ")
                if flag == 2:
                    tmp_arr = line.split("postData")
                    if len(tmp_arr) > 1 and (line.find("industry") != -1 or line.find("query") != -1 or line.find("city") != -1):
                        tmp = tmp_arr[1]
                        tmp = tmp[1:len(tmp)]
                        tmp = json.loads(tmp)
                        if line.find("industry") != -1 and line.find("city") != -1:
                            city_day_industry_map.setdefault(tmp["city"] + '_' + tmp["industry"], 0)
                            city_day_industry_map[tmp["city"] + '_' + tmp["industry"]] += 1
                            city_industry_map.setdefault(tmp["city"] + '_' + tmp["industry"], 0)
                            city_industry_map[tmp["city"] + '_' + tmp["industry"]] += 1
                        elif line.find("city") != -1:
                            city_day_map.setdefault(tmp["city"], 0)
                            city_day_map[tmp["city"]] += 1
                            city_map.setdefault(tmp["city"], 0)
                            city_map[tmp["city"]] += 1
                        elif line.find("industry") != -1:
                            industry = ""
                            if tmp["industry"] != '[]' and len(tmp["industry"]) > 0 and len(tmp["industry"][0]) == 2:
                                industry = tmp["industry"][0]["industry"] + '-' + tmp["industry"][0]["sub_industry"]
                            elif tmp["industry"] != '[]' and len(tmp["industry"]) > 0:
                                industry = tmp["industry"][0]
                            if industry != '':
                                industry_day_map.setdefault(industry, 0)
                                industry_day_map[industry] += 1
                                industry_map.setdefault(industry, 0)
                                industry_map[industry] += 1
                        else:
                            query_day_map.setdefault(tmp["query"], 0)
                            query_day_map[tmp["query"]] += 1
                            query_map.setdefault(tmp["query"], 0)
                            query_map[tmp["query"]] += 1
                    flag = 20
        object_txt.write(stat_day)
        object_txt.write("\r")
        ar = []
        ar = sort_dic(city_day_map)
        if len(ar) > 0:
            for cl in ar:
                tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
                cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
                object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
                object_txt.write("\r")
        # object_txt.write(str(sort_dic(city_day_map)).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
        object_txt.write("\r")

        ar = sort_dic(city_day_industry_map)
        if len(ar) > 0:
            for cl in ar:
                tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
                cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
                object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
                object_txt.write("\r")
        # object_txt.write(str(sort_dic(city_day_industry_map)).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
        object_txt.write("\r")

        ar = sort_dic(query_day_map)
        if len(ar) > 0:
            for cl in ar:
                tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
                cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
                object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
                object_txt.write("\r")
        # object_txt.write(str(sort_dic(query_day_map)).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
        object_txt.write("\r")

        ar = sort_dic(industry_day_map)
        if len(ar) > 0:
            for cl in ar:
                tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
                cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
                object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
                object_txt.write("\r")
        # object_txt.write(str(sort_dic(industry_day_map)).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
        object_txt.write("\r")
        object_txt.write("\r")

    object_txt.write("total:")
    object_txt.write("\r")
    ar = []
    ar = sort_dic(city_map)
    if len(ar) > 0:
        for cl in ar:
            tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
            cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
            object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
            object_txt.write("\r")
    # object_txt.write(str(sort_dic(city_map)).decode('unicode_escape').encode('utf-8').replace('u', '').decode('utf-8').encode('gbk'))
    object_txt.write("\r")
    ar = sort_dic(city_industry_map)
    if len(ar) > 0:
        for cl in ar:
            tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
            cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
            object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
            object_txt.write("\r")
    # object_txt.write(str(sort_dic(city_industry_map)).decode('unicode_escape').encode('utf-8').replace('u', '').decode('utf-8').encode('gbk'))
    object_txt.write("\r")
    ar = sort_dic(query_map)
    if len(ar) > 0:
        for cl in ar:
            tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
            cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
            object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
            object_txt.write("\r")
    # object_txt.write(str(sort_dic(query_map)).decode('unicode_escape').encode('utf-8').replace('u', '').decode('utf-8').encode('gbk'))
    object_txt.write("\r")
    ar = sort_dic(industry_map)
    if len(ar) > 0:
        for cl in ar:
            tmp_cl = str(cl).replace("(", "").replace(")", "").split(",")
            cl = tmp_cl[0].replace("'", "") + '      '+ tmp_cl[1]
            object_txt.write(str(cl).decode('unicode_escape').encode('utf-8').replace('u','').decode('utf-8').encode('gbk'))
            object_txt.write("\r")
    # object_txt.write(str(sort_dic(industry_map)).decode('unicode_escape').encode('utf-8').replace('u', '').decode('utf-8').encode('gbk'))
    object_txt.write("\r")
    object_txt.close()

if __name__ == '__main__':
    main()