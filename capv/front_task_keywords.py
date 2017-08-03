# coding: utf-8

from util import db_util
import datetime
import json

query = db_util.get_product_query()

file_path = 'FrontAna_all.log'

def get_words(keyword):
    # k = keyword.split(":")[1].replace('\n', '').decode('UTF-8')
    # if k == 'null':
    #     k = ' '
    # return '\'' + str(keyword) + '\''
    return keyword


def add_task_keywords():
    file_object = open(file_path)
    for line in file_object:
        task_keywords = line.split(" ")
        if line.find("postData:") == -1:
            continue
        # print line.split("postData:")[1]
        da = json.loads(line.split("postData:")[1])
        uid = 0
        add_task_data_arr = da["add_task_data"]
        if "uid" in da.keys():
            uid = da["uid"]
        # print(add_task_data_arr)
        for add_task_data in add_task_data_arr:
            if "project_id" in add_task_data.keys() and "object_id_list" in add_task_data.keys() and "keywords" in add_task_data.keys():
                # print(da["project_id"], da["object_id_list"], da["keywords"])
                for consultant_id in add_task_data["object_id_list"]:
                    if add_task_data["project_id"] is None:
                        continue
                    time = datetime.datetime.now().strftime('%Y-%m-%d') + " " + task_keywords[0].replace("[","").replace("]", "")
                    sql = ("insert into capvision_fun.clst_search_ana_add_task_tmp(create_time, uid, consultant_id, keywords, task_id, sch_type, module, project_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" %
                           ('\'' + time + '\'',
                            get_words(uid),
                            get_words(consultant_id),
                            '\'' + get_words(add_task_data["keywords"]) + '\'',
                            0, 0, '\'' + 'consultation' + '\'', add_task_data["project_id"],
                            '\'' + 'consultation' + '\''))
                    # print sql
                    try:
                        query.Query(sql)
                    except:
                        print add_task_data_arr
                    # print ('\'' + time + '\'', get_words(uid), get_words(consultant_id), '\'' + get_words(add_task_data["keywords"]) + '\'', 0, 0, 'consultation', add_task_data["project_id"], 'consultation')

        # uid = json.loads(da)["uid"]

if __name__ == '__main__':
    add_task_keywords()
