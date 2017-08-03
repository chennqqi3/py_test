#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys
import json
import MySQLdb
import requests

dic, dic_team, dic_u = {}, {}, {}


def mysql_read(sql, outfn):
    conn = MySQLdb.connect(host='192.168.50.95', port=3306, user='admin', passwd='admin2048az', db='ndb', )
    cur = conn.cursor()
    result = cur.execute(sql)
    OUTFN = open(outfn, 'w')
    for res_row in cur.fetchmany(result):
        print >> OUTFN, re.sub('(\r\n|\n)', '', '<##>'.join([str(el) for el in res_row]), 0)
    cur.close()
    conn.close()


def stk_name_v1():
    tmpfn = '/tmp/stkname1.txt'
    mysql_read('select stockcode,stockname_std,stockname_alias from capvision_fun.dim_stkname_compname',tmpfn)
    dic = {}
    p_stk = '.*?('
    for line in open(tmpfn):
        line = line.strip()
        stockcode,stockname_std,stockname_alias = line.split('<##>')
        for stk_al in stockname_alias.split('.'):
            #if re.match('.*杭州华三',stk_al): print '杭州华三<<<<>>>>>',stk_al,stockname_alias
            dic[stk_al] = [stockcode,stockname_std]
        stockname_alias = re.sub('\.','|',stockname_alias,0) 
        if re.match('.*(银行|证券)', stockname_std): continue

        p_stk += stockname_alias + '|'
    #print p_stk
    return dic, p_stk[:-1] + ')(.*)'




def conslt_stkname(towhere):
    fn,outfn = 'conslt_basic.txt', 'conslt_basic_stkcompany.txt'
    sql = 'select ctid,now_company from capvision_fun.cslt_basic '
    #sql += 'union select ctid,now_company from capvision_fun.cslt_basic_2014 '
    #sql += 'union select ctid,now_company from capvision_fun.cslt_basic_2015 '
    mysql_read(sql, fn)
    OUTFN = open(outfn, 'w')
    dic_stk, p_stk = stk_name_v1()
    for line in open(fn):
        line = line.strip()
        line = re.sub('\s+','',line,0)

        mat = re.match(p_stk, line)
        stkname_alias = mat.group(1) if mat else '##'

        stockcode,stockname_std = dic_stk.get(stkname_alias,['cd','name'])
        #if stkname_alias != '##':
        #    print stkname_alias , stockcode,stockname_std
        #stkname = '会院' if re.match('.*(协会|联合会|研究院|总院)', line.split('<##>')[1]) else stkname
        if towhere == 'uqer':
            print >> OUTFN, stkname_std, stockcode, line.split('<##>')[0]
        if towhere == 'capfun':
            print >> OUTFN, '%s|%s'%(stockname_std,line.split('<##>')[1]),stockcode, line.split('<##>')[0]
            #line.split('<##>')[0]
            #print >>OUTFN,line.split('<##>')[0],line.split('<##>')[1],stkname,dic_stk[stkname],1


def build_comp_stkname(fn):
    sql = 'select id,name from `ndb`.ndb_company_vocabulary;'
    mysql_read(sql, fn)


def read_conslt_company():
    dic_ct = {}
    for line in open('conslt_basic_stkcompany.txt'):
        line = line.strip()
        stkname, stkcd, cid = line.split()
        dic_ct[cid] = [stkcd, stkname]
    return dic_ct


def build_proj_ct():
    sql = "select left(from_unixtime(starttime),10) dt,projectid,consultantid from `ndb`.ndb_project_consultation_task pct join ndb_client cli on pct.clientid=cli.id  "
    #sql += "where from_unixtime(pct.starttime)>='2015-06-01' and from_unixtime(pct.starttime)<'2016-01-01' and cli.type=5;"
    sql += "where from_unixtime(pct.starttime)>='2016-01-01' and from_unixtime(pct.starttime)<'2017-01-01' and cli.type=5;"
    mysql_read(sql, 'proj_const_arrange.txt')


def read_proj_ct():
    dic_proj_ct = {}
    for line in open('proj_const_arrange.txt'):
        dt, projid, cid = line.strip().split('<##>')
        dic_proj_ct.setdefault(projid, [])
        dic_proj_ct[projid].append([cid, dt])
    return dic_proj_ct


def build_npt():
    sql = 'SELECT npt.rid, left(from_unixtime(npt.rtime),10) dt, consultant_hours, ref_projid, npt.rcontent FROM `ndb_sp_npt` npt join ndb_client cli on npt.rclientid=cli.id where type=5'
    mysql_read(sql, 'npt_cont.txt')


def read_npt():
    dic_npt = {}
    for line in open('npt_cont.txt'):
        rid, dt, chours, projid, cont = line.strip().split()[:5]
        if projid == 0 or not projid or projid == 'None': continue
        dic_npt[projid] = [rid, dt, chours, projid, cont]
    return dic_npt


def build_from_demand(demtag, outfn):
    dic_stk, p_stk = stk_name_v1()
    OUTFN = open(outfn,'w')
    tmpfn = '/tmp/tmpfn1.txt'
    if demtag == 'demand_clst':
        sql = "select date,clst_labels,clst_lab_accuracy_mark from capvision_fun.demands where clst_lab_accuracy_mark rlike '.*1' "
    if demtag == 'demand_req':
        sql = "select date,sug_labels,sug_lab_accuracy_mark from capvision_fun.demands where sug_labels !='' "  #sug_lab_accuracy_mark rlike '.*1' "
    mysql_read(sql, tmpfn)
    tit = 'npt_day,secID,secName,num_perbatch,confirm_code, chours'
    print >>OUTFN,tit
    for line in open(tmpfn):
        line = line.strip()
        date,t_labels,t_labels_accuracy = line.split('<##>')
        t_labels_li = t_labels.split(',') #'.'
        t_labels_accuracy_li = t_labels_accuracy.split(',')
        for ii in range(len(t_labels_accuracy_li)):            
            #print >>OUTFN,'%s,%s,%s,%s,%s'%(date, stkcds_li[ii], t_labels_li[ii].split('|')[0].decode('utf-8').encode('gbk'),1,1)
            stkname = t_labels_li[ii].split('|')[0]
            stkcd = dic_stk.get(stkname,['cd','name'])[0]
            confirm_code = t_labels_accuracy_li[ii]
            print >>OUTFN,'%s,%s,%s,%s,%s,%s'%(date, stkcd,stkname.decode('utf-8').encode('gbk'),1,confirm_code,1)


def build_from_npt():
    dic_stk, p_stk = stk_name()
    tit = 'npt_day,secID,secName,num_perbatch,chours'
    print tit
    for line in open(fn):
        line = line.strip()
        rid, date, chours = line.split()[:3]
        nline = line
        mat = re.match(p_stk, nline)
        stkcds, stknames = [], []
        while mat:
            stkname = mat.group(1)
            if stkname not in stknames:
                stknames.append(stkname)
                stkcds.append(dic_stk[stkname])
            nline = mat.group(2)
            mat = re.match(p_stk, nline)
        if stkcds:
            # print '%s,%s,%s'%(rid, '.'.join(stkcds), '.'.join(stknames))
            for jj in range(len(stkcds)):
                print '%s,%s,%s,%s,%s' % (date, stkcds[jj], stknames[jj].decode('utf-8').encode('gbk'), len(stkcds), chours)


def build_from_clst(towhere):
    dic_ct = read_conslt_company()
    dic_proj_ct = read_proj_ct()
    dic_npt = read_npt()
    if towhere=='uqer': print 'npt_day,secID,secName,v1,chours'
    for projid in dic_proj_ct:
        if projid == 0 or not projid or projid == 'None': continue
        isnpt = 1 if projid in dic_npt else 0
        # if isnpt ==0:continue
        # if int(chours)==0:continue
        stkcds, stknames = [], []
        for cid, dt in dic_proj_ct[projid]:
            # if dt <'2016-02-01':continue
            if cid in dic_ct:
                #if dic_ct[cid][0] not in stkcds: 

                if dic_ct[cid][1] not in stknames: 
                    stkcds.append(dic_ct[cid][0])
                    stknames.append(dic_ct[cid][1])
                if towhere == 'uqer':
                    print '%s,%s,%s,%s,%s' % (dt, dic_ct[cid][0], dic_ct[cid][1].decode('utf-8').encode('gbk'), isnpt, 0)
        if towhere == 'capfun':
            stknames_str = ';'.join(stknames)
            stknames_str = re.sub('(有限公司|公司|股份有限公司|技术有限公司|有限责任|集团)','',stknames_str,0)
            print '%s,%s,%s'%(projid,';'.join(stkcds), stknames_str)


def upload(fn):
    cookies = {'cloud-anonymous-token': '460da3ca1d2c46a89c2e52b03c934be3', 'cloud-sso-token': '3765750820A1244787425D860C0D4A56'}
    r = requests.post('https://gw.wmcloud.com/mercury/api/databooks',                  files={'datafile': open(fn, 'rb')},                  cookies=cookies                  )
    print(r.text)
# build_comp_vocab_stkname(fn)

#conslt_stkname('capfun')
#build_proj_ct()
ctype = sys.argv[1]
if ctype == 'stk_proj':
    build_from_clst('capfun')
if ctype == 'demand_clst':
    fn = sys.argv[2]
    build_from_demand(ctype,fn)
    #upload(fn)
if ctype == 'demand_req':
    fn = sys.argv[2]
    build_from_demand(ctype,fn)
    #upload(fn)
   
