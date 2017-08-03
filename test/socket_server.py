#!/usr/bin/python
# coding=utf-8

import re
import urllib,urllib2


def translate(text):
    text_1=text
     #'langpair':'en'|'zh-CN'从英语到简体中文
    values={'hl':'zh-CN','ie':'UTF-8','text':text_1,'langpair':"'en'|'zh-CN'"}
    url='http://translate.google.cn/translate_t'
    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
     #模拟一个浏览器
    browser='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
    req.add_header('User-Agent',browser)
     #向谷歌翻译发送请求
    response = urllib2.urlopen(req)
     #读取返回页面
    html=response.read()
    print html
    p=re.compile(r"(?<=TRANSLATED_TEXT=).*?;")
    m=p.search(html)
    text_2=m.group(0).strip(';')
    return text_2

if __name__ == "__main__":
         #text_1 原文
     #text_1=open('c:\\text.txt','r').read()
    text_1='Hello, my name is Derek. Nice to meet you! '
    print('The input text: %s' % text_1)
    text_2=translate(text_1).strip("'")
    print('The output text: %s' % text_2)

     #保存结果
     # filename='c:\\Translation.txt'
     # fp=open(filename,'w')
     # fp.write(text_2)
     # fp.close()

     # report='Master, I have done the work and saved the translation at '+filename+'.'
     # print('Report: %s' % report)