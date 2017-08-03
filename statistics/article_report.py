# coding=utf-8

import os
import time
import json
from util import db_util

query = db_util.get_query()


def analysis(uv_dic):
    dic = {}
    for key, count in uv_dic.items():
        uid, article_id = key.split("_")
        dic.setdefault(article_id, 0)
        dic[article_id] += 1
    return dic


def insert_data(date, article_id, title, column, topic, client_pv, client_uv, consultant_pv, consultant_uv, visitor_pv,
                visitor_uv, tourist_pv, tourist_uv):
    query.Query(
        " insert INTO ks_data_statistics.ks_article_report(statday, article_id, title, colunm, topic, client_pv, client_uv, consultant_pv, consultant_uv, visitor_pv, visitor_uv, tourist_pv, tourist_uv) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate KEY UPDATE statday = %s" %
        ('\'' + date + '\'', article_id, '\'' + title + '\'', '\'' + column + '\'', '\'' + topic + '\'', client_pv,
         client_uv, consultant_pv, consultant_uv,
         visitor_pv, visitor_uv, tourist_pv, tourist_uv, '\'' + date + '\'')
    )


def check_article(id):
    query1 = db_util.get_product_query()
    article_detail = {}
    query1.Query('select * from ksexpt.ks_article where article_id = %s' %
                 (id))
    for row in query.record:
        article_detail = dict(article_id=row['article_id'], category_name=row['category_name'],
                              category_id=row['category_id'], article_title=row['article_title'])
    return article_detail


def check_topic(id):
    topic_detail = {}
    query.Query('select * from ksexpt.ks_special_topic where id = %s' %
                (id))
    for row in query.record:
        topic_detail = dict(id=row['id'], special_topic_name=row['special_topic_name'])
    return topic_detail


def main():
    # path = '/data/logs/ks_stat/'
    path = 'c:\\'

    if not os.path.isdir(path):
        print 'no stat'
        return

    stat_file_list = []
    files = os.listdir(path)
    print files
    for f in files:
        if os.path.isfile(path + '/' + f):
            if f[0:8] == 'log.log.':
                stat_file_list.append(f)

    topic_dic = {}
    topic_arr = []
    # stat_file_list.append('log.log')
    for pth in stat_file_list:
        stat_day = pth.replace('log', '').replace('.', '')
        if stat_day == '':
            stat_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        with open(path + pth) as file_object:
            client_pv = {}
            consultant_pv = {}
            visitor_pv = {}
            tourist_pv = {}
            client_uv = {}
            consultant_uv = {}
            visitor_uv = {}
            tourist_uv = {}
            flag = 20
            dic_line = []
            key_value = {}
            for line in file_object:
                line = line.strip()
                flag += 1
                if line.find("/ks_web/api/common/article/content") != -1:
                    flag = 0
                    key_value = {}
                if flag == 1:
                    tmp_arr = line.split(" ")
                    key = tmp_arr[4:9]
                    key_value.setdefault("key", key)
                    key_value["key"] = key
                if flag == 2:
                    if line.find('"articleid":') != -1:
                        tmp_arr = line.split("postData:")
                        tmp = tmp_arr[1].replace(" ", "")
                        jo = json.loads(tmp)
                        article_id = jo["articleid"]
                        article_id = str(article_id)
                        key_value.setdefault("articleid", article_id)
                        key_value["articleid"] = article_id
                        dic_line.append(key_value)
                        if "navigation_id" in jo.keys():
                            navigation_id = str(jo["navigation_id"])
                            if navigation_id.find("$") != -1 and navigation_id not in topic_arr:
                                topic_arr.append(navigation_id)
                                topic_detail = check_topic(navigation_id.replace("$", ""))
                                if len(topic_detail) > 0:
                                    topic_dic.setdefault(article_id, "")
                                    topic_dic[article_id] = topic_detail["special_topic_name"]
                    flag = 20

            articleid_arr = []
            for key_value in dic_line:
                key = key_value["key"]
                articleid = key_value["articleid"]
                if articleid.isdigit():
                    articleid_arr.append(articleid)
                uid = key[0].replace('uid:', '').replace(',', '')
                role = key[4].replace('role:', '')
                dup_pv = articleid
                dup_uv = uid + '_' + articleid
                if role == 'client':
                    client_pv.setdefault(dup_pv, 0)
                    client_pv[dup_pv] += 1
                    client_uv.setdefault(dup_uv, 0)
                    client_uv[dup_uv] += 1
                elif role == 'consultant':
                    consultant_pv.setdefault(dup_pv, 0)
                    consultant_pv[dup_pv] += 1
                    consultant_uv.setdefault(dup_uv, 0)
                    consultant_uv[dup_uv] += 1
                elif role == 'visitor':
                    visitor_pv.setdefault(dup_pv, 0)
                    visitor_pv[dup_pv] += 1
                    visitor_uv.setdefault(dup_uv, 0)
                    visitor_uv[dup_uv] += 1
                else:
                    tourist_pv.setdefault(dup_pv, 0)
                    tourist_pv[dup_pv] += 1
                    tourist_uv.setdefault(dup_uv, 0)
                    tourist_uv[dup_uv] += 1

            client_uv = analysis(client_uv)
            consultant_uv = analysis(consultant_uv)
            visitor_uv = analysis(visitor_uv)
            tourist_uv = analysis(tourist_uv)

            for article_id in articleid_arr:
                client_pv_count = 0
                client_uv_count = 0
                consultant_pv_count = 0
                consultant_uv_count = 0
                visitor_pv_count = 0
                visitor_uv_count = 0
                tourist_pv_count = 0
                tourist_uv_count = 0
                if len(client_pv) > 0:
                    if article_id in client_pv.keys():
                        client_pv_count = client_pv[article_id]
                if len(client_uv) > 0:
                    if article_id in client_uv.keys():
                        client_uv_count = client_uv[article_id]
                if len(consultant_pv) > 0:
                    if article_id in consultant_pv.keys():
                        consultant_pv_count = consultant_pv[article_id]
                if len(consultant_uv) > 0:
                    if article_id in consultant_uv.keys():
                        consultant_uv_count = consultant_uv[article_id]
                if len(visitor_pv) > 0:
                    if article_id in visitor_pv.keys():
                        visitor_pv_count = visitor_pv[article_id]
                if len(visitor_uv) > 0:
                    if article_id in visitor_uv.keys():
                        visitor_uv_count = visitor_uv[article_id]
                if len(tourist_pv) > 0:
                    if article_id in tourist_pv.keys():
                        tourist_pv_count = tourist_pv[article_id]
                if len(tourist_uv) > 0:
                    if article_id in tourist_uv.keys():
                        tourist_uv_count = tourist_uv[article_id]

                print stat_day
                topic_name = ""
                if article_id in topic_dic.keys():
                    topic_name = topic_dic[article_id]

                article_detail = check_article(article_id)
                if len(article_detail) == 0:
                    continue

                print article_id
                print article_detail["article_title"]
                print article_detail["category_name"]
                print topic_name
                insert_data(stat_day, article_id, article_detail["article_title"],
                            article_detail["category_name"], topic_name, client_pv_count, client_uv_count,
                            consultant_pv_count, consultant_uv_count, visitor_pv_count,
                            visitor_uv_count, tourist_pv_count, tourist_uv_count)


if __name__ == '__main__':
    main()
