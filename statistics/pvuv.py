# coding=utf-8
from util import db_util

query = db_util.get_query()


def pvuv(path, stat_file_list):
    file_object = open(path+"stat.log")

    tot_pv_map = {}
    tot_uv_map = {}
    ios_pv_map = {}
    ios_uv_map = {}
    and_pv_map = {}
    and_uv_map = {}
    client_pv_map = {}
    client_uv_map = {}
    consultant_pv_map = {}
    consultant_uv_map = {}
    visitor_pv_map = {}
    visitor_uv_map = {}
    tourist_pv_map = {}
    tourist_uv_map = {}

    try:
        for f in stat_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                time = arr[0][0:10]
                if arr[1] == 'null':
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                ak = arr[1][2:3]
                uid = arr[3]
                role = arr[2]
                device = arr[4]
                url = arr[5]
                tot_pv_map.setdefault(time, 0)
                tot_pv_map[time] += 1
                tot_uv_map.setdefault(time+','+device, 0)
                tot_uv_map[time+','+device] += 1
                if ak == '2':
                    ios_pv_map.setdefault(time, 0)
                    ios_pv_map[time] += 1
                if ak == '2':
                    ios_uv_map.setdefault(time+','+device, 0)
                    ios_uv_map[time+','+device] += 1
                if ak == '1':
                    and_pv_map.setdefault(time, 0)
                    and_pv_map[time] += 1
                if ak == '1':
                    and_uv_map.setdefault(time+','+device, 0)
                    and_uv_map[time+','+device] += 1
                if role == 'client':
                    client_pv_map.setdefault(time, 0)
                    client_pv_map[time] += 1
                if role == 'client':
                    client_uv_map.setdefault(time+','+device, 0)
                    client_uv_map[time+','+device] += 1
                if role == 'consultant':
                    consultant_pv_map.setdefault(time, 0)
                    consultant_pv_map[time] += 1
                if role == 'consultant':
                    consultant_uv_map.setdefault(time+','+device, 0)
                    consultant_uv_map[time+','+device] += 1

                if role == 'visitor':
                    visitor_pv_map.setdefault(time, 0)
                    visitor_pv_map[time] += 1
                if role == 'visitor':
                    visitor_uv_map.setdefault(time+','+device, 0)
                    visitor_uv_map[time+','+device] += 1

                if role == 'tourist':
                    tourist_pv_map.setdefault(time, 0)
                    tourist_pv_map[time] += 1
                if role == 'tourist':
                    tourist_uv_map.setdefault(time+','+device, 0)
                    tourist_uv_map[time+','+device] += 1

    finally:
        file_object.close()

    tot_uv_map = clear_count(tot_uv_map)
    ios_uv_map = clear_count(ios_uv_map)
    and_uv_map = clear_count(and_uv_map)
    client_uv_map = clear_count(client_uv_map)
    consultant_uv_map = clear_count(consultant_uv_map)
    visitor_uv_map = clear_count(visitor_uv_map)
    tourist_uv_map = clear_count(tourist_uv_map)

    insert(tot_pv_map, 'tot_pv')
    insert(tot_uv_map, 'tot_uv')
    insert(ios_pv_map, 'ios_pv')
    insert(ios_uv_map, 'ios_uv')
    insert(and_pv_map, 'and_pv')
    insert(and_uv_map, 'and_uv')
    insert(client_pv_map, 'client_pv')
    insert(client_uv_map, 'client_uv')
    insert(consultant_pv_map, 'consultant_pv')
    insert(consultant_uv_map, 'consultant_uv')
    insert(visitor_pv_map, 'visitor_pv')
    insert(visitor_uv_map, 'visitor_uv')
    insert(tourist_pv_map, 'tourist_pv')
    insert(tourist_uv_map, 'tourist_uv')


def clear_count(dic):
    tot_map = {}
    for time, c in dic.items():
        time = time.split(',')[0]
        tot_map.setdefault(time, 0)
        tot_map[time] += 1
    return tot_map


def insert(dic, tp):
    for time, c in dic.items():
        query.Query(
            " insert INTO ks_data_statistics.ks_pvuv(statday, %s) "
            "VALUES (%s, %s) on duplicate KEY UPDATE %s = %s" %
            (tp, '\''+time+'\'', c, tp, c)
        )

if __name__ == '__main__':
    pvuv()