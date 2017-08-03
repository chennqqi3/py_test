# coding: utf-8

from util import db_util
import datetime

query = db_util.get_dev_query()

dat = "2016-12-26"

file_path = 'consultant_click.log.' + dat


def get_words(keyword):
    k = keyword.split(":")[1].replace('\n', '').decode('UTF-8')
    if k == 'null':
        k = ' '
    return '"' + k + '"'


def add_task_keywords():
    file_object = open(file_path)
    for line in file_object:
        task_keywords = line.split(" ")
        print line
        if len(task_keywords) != 3:
            continue
        keywords_arr = task_keywords[2].split(",")
        time = dat + " " + task_keywords[0].replace("[","").replace("]", "")
        if len(keywords_arr) == 3:
            uid, consultant_id, key_words = task_keywords[2].split(",")
            query.Query("insert into ndb.ndb_consultant_click_log_copy(create_time, uid, consultant_id, key_words) VALUES (%s, %s, %s, %s)" %
                        ('\'' + time + '\'', get_words(uid), get_words(consultant_id), get_words(key_words)))
if __name__ == '__main__':
    add_task_keywords()
