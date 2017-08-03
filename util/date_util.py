# coding=utf-8
import datetime


def date_add(time, day):
    y, m, d = time.split('-')
    d = datetime.datetime(int(y), int(m), int(d))
    d2 = d + datetime.timedelta(day)
    return d2

if __name__ == '__main__':
    date_add('2015-01-01', 3)
