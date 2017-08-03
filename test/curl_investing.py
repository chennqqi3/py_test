#!/usr/bin/env python
import sys
import os
import os.path
import requests
import re
from bs4 import BeautifulSoup



def curl_tit(code):
    # domain = 'http://www.investing.com/'
    # url = domain+'indices/major-indices'
    domain = 'http://finance.sina.com.cn/realstock/company/sh{code}/nc.shtml'
    url = domain.replace('{code}', code)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser', from_encoding="UTF-8")
    div = soup.find("div", id="hqDetails")
    print div
    # table = soup.find("table", id="cr_12")
    # tds = table.find_all('td')
    # for tr in tds:
    #     print tr

    # Fout = open('major_index.html','w')
    # for el in url_list[:60]:
    #     code,cd_url,stk_descr = el
    #     r = requests.get(cd_url)
    #     soup = BeautifulSoup(r.text, 'html.parser')
    #     ele = soup.find('th',text=re.compile("Capitalisation"))
    #     cap = ele.parent.td.text
    #     cap =re.sub(',','',cap[1:],0)
    #     cap = int(cap)/1000/100
        # print >>Fout, '<a href="%s/markets/NZSX/securities/%s">%s %s %s </a><br/>'%(domain,code, code,cap,stk_descr)


curl_tit("603568")