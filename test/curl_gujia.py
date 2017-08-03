# coding: utf-8

from bs4 import BeautifulSoup
import requests


def curl_gu(stk_cd):
    url= 'http://www.sogou.com/sie?ekv=2&ie=utf8&query=%s' % stk_cd
    print url
    sess = requests.session()
    r = sess.get(url)
    soup=BeautifulSoup(r.text, 'lxml', from_encoding="utf-8")
    divs = soup.find_all("h3", attrs={'class': 'vrTitle'})
    print(divs)

if __name__ == '__main__':
    curl_gu('股价 百度')

