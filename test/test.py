# coding: utf-8

from bs4 import BeautifulSoup
import requests

def curl_tit(stk_cd):
    url= 'http://basic.10jqka.com.cn/%s/company.html' % stk_cd
    print url
    sess = requests.session()
    r = sess.get(url)
    soup=BeautifulSoup(r.text, 'lxml', from_encoding="gbk")
    # soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.find_all("div", attrs={'class': 'bd'})
    print(divs[1].select('table')[0].select('tr')[2].select('td')[0].select('span')[0].string.strip())


def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i*i
        fs.append(f)
    return fs



if __name__ == '__main__':
    # curl_tit('600511')
    # curl_tit('002456')
    # curl_tit('002561')
    # curl_tit('000970')
    # curl_tit('000910')
    # curl_tit('000895')
    print count()

