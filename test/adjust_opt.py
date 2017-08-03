#!/usr/bin/env python
import sys
import os
import os.path
import requests
from bs4 import BeautifulSoup

exchng = sys.argv[1]
srcdir = sys.argv[2]
targdir = sys.argv[3]
startyear = sys.argv[4]

def curl(exchng,srcdir):
    fn='%s_stkcd_top200.txt'%exchng
    for line in open(fn):
        stkcd = line.strip()
        url = 'http://ichart.yahoo.com/table.csv?s=%s&a=0&b=1&c=%s&g=d&ignore=.csv'%(stkcd,startyear)
        r = requests.get(url)
        FIN = open(srcdir + '/' + stkcd + '.csv','w')
        print stkcd,url
        print >>FIN, r.text,
        FIN.close()
        #break
    
def adj(srcdir, targdir):
    for parent,dirnames,filenames in os.walk(srcdir):
        for filename in filenames:
            dic={'m':{},'q':{}}
            stkcd = filename[:-4]
            #if stkcd != 'AAPL':continue
            FIN = open(srcdir+'/'+filename)
            FOU = open(targdir+'/d_'+filename,'w')

            print >>FOU,'date,open,high,low,close,volume,vol2'
            for line in FIN:
                line = line.strip()
                #print line
                data= line.split(',')
                if data[0] == 'Date':continue
                if len(data) < 6: continue
                op,hi,lo,cl,vol,cl_j = [float(el) for el in data[1:]]
                date = data[0]
                vol = int(vol)
                cl_j = cl_j
                op_j = op * (cl_j/cl)
                hi_j = hi * (cl_j/cl)
                lo_j = lo * (cl_j/cl)
                print >>FOU, '%s,%.3f,%.3f,%.3f,%.3f,%d'%(date,op_j,hi_j,lo_j,cl_j,vol)

                month = date[:7]
                qt = date[:4] + '-' + str(int((int(month[-2:])-1)/3)*3+101)[1:]
                dic['m'].setdefault(month,{})
                dic['q'].setdefault(qt,{})
                dic['m'][month].setdefault('op',op_j)
                dic['m'][month].setdefault('hi',hi_j)
                dic['m'][month].setdefault('lo',lo_j)
                dic['m'][month].setdefault('cl',cl_j)
                dic['m'][month].setdefault('vol',100)
                dic['m'][month].setdefault('vol2',10)
                dic['q'][qt].setdefault('op',op_j)
                dic['q'][qt].setdefault('hi',hi_j)
                dic['q'][qt].setdefault('lo',lo_j)
                dic['q'][qt].setdefault('cl',cl_j)
                dic['q'][qt].setdefault('vol',100)
                dic['q'][qt].setdefault('vol2',10)
                #dic[month]['vol'] +=vol
                if dic['m'][month]['hi']<hi_j: dic['m'][month]['hi']=hi_j
                if dic['m'][month]['lo']>lo_j: dic['m'][month]['lo']=lo_j
                dic['m'][month]['cl']=cl_j
                if dic['q'][qt]['hi']<hi_j: dic['q'][qt]['hi']=hi_j
                if dic['q'][qt]['lo']>lo_j: dic['q'][qt]['lo']=lo_j
                dic['q'][qt]['cl']=cl_j

            FOU.close()
            FIN.close()


            FOU = open(targdir+'/m_'+filename,'w')
            print >>FOU,'date,open,high,low,close,volume,vol2'
            dic_m =dic['m']
            for jmon in sorted(dic_m.keys(),reverse=True):
                print >>FOU, '%s-01,%.3f,%.3f,%.3f,%.3f,%d,%d'%(jmon,dic_m[jmon]['op'],dic_m[jmon]['hi'],dic_m[jmon]['lo'],dic_m[jmon]['cl'],dic_m[jmon]['vol'],dic_m[jmon]['vol2'])
            FOU.close()


            FOU = open(targdir+'/q_'+filename,'w')
            print >>FOU,'date,open,high,low,close,volume,vol2'
            dic_q = dic['q']
            for jqt in sorted(dic_q.keys(),reverse=True):
                print >>FOU, '%s-01,%.3f,%.3f,%.3f,%.3f,%d,%d'%(jqt,dic_q[jqt]['op'],dic_q[jqt]['hi'],dic_q[jqt]['lo'],dic_q[jqt]['cl'],dic_q[jqt]['vol'],dic_q[jqt]['vol2'])
            FOU.close()


def get_symbol(exchng):
    arr = []
    fn = '%s_stkcd_top200.txt'%exchng
    url = 'http://sg.finance.yahoo.com/q/cp?s=%5ESTI'
    r = requests.get(url)
    r = BeautifulSoup(r.text, 'lxml')
    for rr in r.find_all("table", class_='yfnc_tableout1')[0].select('table')[0].select('tr'):
        tds = rr.select('td')
        if len(tds) == 0:
            continue
        c = tds[0].select('b')[0].select('a')[0]
        arr.append(c.string.strip())

    print arr
    if len(arr) > 0:
        with open(fn, "w") as f:
            f.write("")
        output = open(fn, 'a')
        for symbol in arr:
            output.write(symbol)
            output.write("\n")


get_symbol(exchng)
curl(exchng,srcdir)
#adj(srcdir,targdir)
