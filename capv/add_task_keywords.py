# coding: utf-8

from util import db_util
import datetime

query = db_util.get_product_query()

file_path = 'add_task.log.2016-12-24'


def get_words(keyword):
    k = keyword.split(":")[1].replace('\n', '').decode('UTF-8')
    if k == 'null':
        k = ' '
    return '\'' + k + '\''


def add_task_keywords():
    file_object = open(file_path)
    for line in file_object:
        task_keywords = line.split(" ")
        print line
        if len(task_keywords) != 3:
            continue
        keywords_arr = task_keywords[2].split(",")
        if len(keywords_arr) != 5:
            continue
        # time = datetime.datetime.now().strftime('%Y-%m-%d') + " " + task_keywords[0].replace("[","").replace("]", "")
        time = '2016-12-24' + " " + task_keywords[0].replace("[","").replace("]", "")
        uid, consultant_id, key_words, task_id, module = task_keywords[2].split(",")
        query.Query("insert into capvision_fun.cslt_search_ana_add_task(create_time, uid, consultant_id, keywords, task_id, sch_type, module) VALUES (%s, %s, %s, %s, %s, %s, %s) on duplicate key update module = %s" %
                    ('\'' + time + '\'', get_words(uid), get_words(consultant_id), get_words(key_words), get_words(task_id), 0, get_words(module), get_words(module)))

    query.Query("DELETE FROM capvision_fun.cslt_search_ana_add_task WHERE keywords = ''")
    query.Query("INSERT into capvision_fun.cslt_search_kw_add_task (SELECT * FROM cslt_search_ana_add_task GROUP BY keywords)")
if __name__ == '__main__':
    add_task_keywords()
