# coding: utf-8

from util import db_util

query = db_util.get_product_query()

file_path = 'add_task.log.2016-12-24'

def add_log():
    file_object = open(file_path)
    for line in file_object:
        task_keywords = line.split(" ")
        print line


if __name__ == '__main__':
    add_log()
