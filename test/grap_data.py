__author__ = 'dhu'

import urllib2
import re

if __name__ == '__main__':
    html = ""
    for line in urllib2.urlopen("http://finance.yahoo.com/q/cp?s=%5EGDAXI"):
        line = line.decode('utf-8')
        html = html + line
        print line