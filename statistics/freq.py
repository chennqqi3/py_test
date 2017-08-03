# coding=utf-8
from util import db_util

query = db_util.get_query()


# 活跃设备数
def freq(path, stat_file_list):
    file_object = open(path+"stat.log")

    date_map = {}
    date_ak_map = {}
    date_uid_map = {}
    date_plant_uid_map = {}

    try:
        for f in stat_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                if len(arr) != 7:
                    continue
                time = arr[0][0:10]
                if arr[1] == 'null':
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                ak = arr[1][2:3]
                # 设备号
                uid = arr[4]
                date_plant_uid = time + 's' + ak + 's' + uid
                date_uid = time + "s" + uid
                date_uid_map.setdefault(date_uid, 0)
                date_plant_uid_map.setdefault(date_plant_uid, 0)
                date_plant_uid_map[date_plant_uid] = 1
                date_uid_map[date_uid] = 1
                date_map[time] = 0
                date_ak_map[time + 's' + ak] = 0

    finally:
        file_object.close()

    par_date_map = []
    for date, count in date_map.items():
        par_date_map.append(date)
        freq_tot(date_uid_map, par_date_map)

    for date_ak, count in date_ak_map.items():
        tmp_map = []
        tmp_date, ak = date_ak.split('s')
        for date, c in date_map.items():
            if date == tmp_date:
                tmp_map.append(date)
                break
            tmp_map.append(date)
        freq_plant(date_plant_uid_map, tmp_map, date_ak[11:12])


def freq_tot(date_uid_map, date_map):
    uid_count = {}
    group_count = {}
    for date, count in date_uid_map.items():
        print date
        d_time, uid = date.split("s")
        if d_time in date_map:
            uid_count.setdefault(uid, 0)
            uid_count[uid] += 1

    for uid, c in uid_count.items():
        group_count.setdefault(c, 0)
        group_count[c] += 1

    date_type = ["d1", "d2", "d3", "d4", "d5", "d6-d10", "d11-d20", "d21-d30"]

    # for freq_type in date_type:
    #     query.Query(
    #         " insert INTO ks_data_statistics.ks_freq(statday, freq_type) "
    #         "VALUES (%s, %s) on duplicate KEY UPDATE freq_type = %s" %
    #         ('\''+date_map[len(date_map) - 1]+'\'', '\''+freq_type+'\'', '\''+freq_type+'\'')
    #     )

    for num, c in group_count.items():
        freq_type = ''
        if num == 1:
            freq_type = 'd1'
        elif num == 2:
            freq_type = 'd2'
        elif num == 3:
            freq_type = 'd3'
        elif num == 4:
            freq_type = 'd4'
        elif num == 5:
            freq_type = 'd5'
        elif num == 6:
            freq_type = 'd6-d10'
        elif num == 11:
            freq_type = 'd11-d20'
        elif num == 21:
            freq_type = 'd21-d30'

        # query.Query(
        #     " insert INTO ks_data_statistics.ks_freq(statday, freq_type, tot_num) "
        #     "VALUES (%s, %s, %s) on duplicate KEY UPDATE tot_num = %s" %
        #     ('\''+date_map[len(date_map) - 1]+'\'', '\''+freq_type+'\'', c, c)
        # )


def freq_plant(date_plant_uid_map, date_map, ak):
    uid_count = {}
    group_count = {}
    for date, count in date_plant_uid_map.items():
        d_time, d_ak, d_uid = date.split('s')
        if d_time in date_map and d_ak == ak:
            uid_count.setdefault(d_uid, 0)
            uid_count[d_uid] += 1
    for uid, c in uid_count.items():
        group_count.setdefault(c, 0)
        group_count[c] += 1

    for num, c in group_count.items():
        freq_type = ''
        if num == 1:
            freq_type = 'd1'
        elif num == 2:
            freq_type = 'd2'
        elif num == 3:
            freq_type = 'd3'
        elif num == 4:
            freq_type = 'd4'
        elif num == 5:
            freq_type = 'd5'
        elif num == 6:
            freq_type = 'd6-d10'
        elif num == 11:
            freq_type = 'd11-d20'
        elif num == 21:
            freq_type = 'd21-d30'

        # if ak == '1' and freq_type != '':
        #     query.Query(
        #         " insert INTO ks_data_statistics.ks_freq(statday, freq_type, and_num) "
        #         "VALUES (%s, %s, %s) on duplicate KEY UPDATE and_num = %s" %
        #         ('\''+date_map[len(date_map) - 1]+'\'', '\''+freq_type+'\'', c, c)
        #     )
        # elif ak == '2' and freq_type != '':
        #     query.Query(
        #         " insert INTO ks_data_statistics.ks_freq(statday, freq_type, ios_num) "
        #         "VALUES (%s, %s, %s) on duplicate KEY UPDATE ios_num = %s" %
        #         ('\''+date_map[len(date_map) - 1]+'\'', '\''+freq_type+'\'', c, c)
        #     )
