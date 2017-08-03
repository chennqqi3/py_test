#!/usr/bin/env python
# coding: utf-8

import datetime
import json
import re


def add_task_keywords():
    OUTFN = open('fa_add_task.csv', 'w')
    dic_kw = {}
    for line in open('fa_add_task.log'):
        print line
        date,time,jdata = line.split("\t")
        date = date[:10]
        if date <'2016-10-01':continue
        dt = '%s %s'%(date, time)
        da = json.loads(jdata)
        uid = da.get('uid', 0)
        if not da["add_task_data"]: continue
        add_task_data = da["add_task_data"][-1]
        project_id = add_task_data.get('project_id', 0)
        clst_ids = add_task_data.get('object_id_list', [])
        keyword = add_task_data.get('keywords', '')
        if not keyword: keyword = da.get('keywords', '')
        if not keyword or isinstance(keyword, list): continue
        dic_kw.setdefault(keyword.encode('utf-8'), 0)
            # print keyword
        keyword = re.sub('\s+', ',', keyword.encode('utf-8'))

        for clst_id in clst_ids:
            print >>OUTFN, ','.join([dt,str(uid),str(project_id),str(clst_id),keyword])

    print len(dic_kw)


if __name__ == '__main__':
    add_task_keywords()

