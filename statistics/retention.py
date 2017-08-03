# coding=utf-8
from util import db_util
from util import date_util

query = db_util.get_query()


# APP留存
def retention(path, stat_file_list):
    file_object = open(path+"stat.log")

    date_array = []
    date_uid_array = []
    date_plant_uid_array = []

    try:
        for f in stat_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                if arr[1] == 'null':
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                time = arr[0][0:10]
                uid = arr[3]
                ak = arr[1][2:3]
                date_array.append(time)
                date_uid_array.append(time + 's' + uid)
                date_plant_uid_array.append(time + 's' + ak + 's' + uid)

        date_array = set(date_array)
        date_uid_array = set(date_uid_array)
        date_plant_uid_array = set(date_plant_uid_array)

        # print date_array, date_uid_array, date_plant_uid_array
        print '----------------------------------------------------------'

        for time in date_array:
            calc_retention('d2', time, date_util.date_add(time, 1), date_uid_array)
            # calc_retention('d7', time, date_util.date_add(time, 7), date_uid_array)
            # calc_retention('d30', time, date_util.date_add(time, 30), date_uid_array)
            # calc_retention('d90', time, date_util.date_add(time, 90), date_uid_array)
            # calc_retention('d180', time, date_util.date_add(time, 180), date_uid_array)
            # calc_retention('d360', time, date_util.date_add(time, 360), date_uid_array)

        for time in date_array:
            calc_plant_retention('d2', time, date_util.date_add(time, 1), date_plant_uid_array)
            # calc_plant_retention('d7', time, date_util.date_add(time, 7), date_plant_uid_array)
            # calc_plant_retention('d30', time, date_util.date_add(time, 30), date_plant_uid_array)
            # calc_plant_retention('d90', time, date_util.date_add(time, 90), date_plant_uid_array)
            # calc_plant_retention('d180', time, date_util.date_add(time, 180), date_plant_uid_array)
            # calc_plant_retention('d360', time, date_util.date_add(time, 360), date_plant_uid_array)

    finally:
        file_object.close()
    return ""


def calc_retention(retention_type, time1, time2, date_uid_array):
    tmp_uid1 = []
    tmp_uid2 = []
    for date_uid in date_uid_array:
        date, uid = date_uid.split('s')
        if time1 == date:
            tmp_uid1.append(uid)

    for date_uid in date_uid_array:
        date, uid = date_uid.split('s')
        if str(time2)[0:10] == date and uid in tmp_uid1:
            tmp_uid2.append(uid)

    print tmp_uid1, tmp_uid2
    # query.Query(
    #     " insert INTO ks_data_statistics.ks_retention(statday, retent_type, tot_init_num, tot_percent) "
    #     "VALUES (%s, %s, %s, %s) on duplicate KEY UPDATE tot_init_num = %s, tot_percent = %s" %
    #     ('\''+time1+'\'', '\''+retention_type+'\'', len(tmp_uid2), float(len(tmp_uid2)) / float(len(tmp_uid1)), len(tmp_uid2),
    #      float(len(tmp_uid2)) / float(len(tmp_uid1)))
    # )


def calc_plant_retention(retention_type, time1, time2, date_plant_uid_array):
    tmp_uid_ak1 = []
    tmp_uid_ak_retention1 = []
    tmp_uid_ak2 = []
    tmp_uid_ak_retention2 = []
    for date_plant_uid in date_plant_uid_array:
        date, ak, uid = date_plant_uid.split('s')
        if time1 == date:
            if ak == '1':
                tmp_uid_ak1.append(uid)
            elif ak == '2':
                tmp_uid_ak2.append(uid)

    for date_plant_uid in date_plant_uid_array:
        date, ak, uid = date_plant_uid.split('s')
        if str(time2)[0:10] == date and ak == '1' and uid in tmp_uid_ak1:
            tmp_uid_ak_retention1.append(uid)
        elif str(time2)[0:10] == date and ak == '2' and uid in tmp_uid_ak2:
            tmp_uid_ak_retention2.append(uid)

    tmp_per2 = 0
    if len(tmp_uid_ak2) == 0:
        tmp_per2 = 0
    else:
        tmp_per2 = float(len(tmp_uid_ak_retention2)) / float(len(tmp_uid_ak2))

    print time1, retention_type, len(tmp_uid_ak_retention2), tmp_per2
    # query.Query(
    #     " insert INTO ks_data_statistics.ks_retention(statday, retent_type, ios_init_num, ios_percent) "
    #     "VALUES (%s, %s, %s, %s) on duplicate KEY UPDATE ios_init_num = %s, ios_percent = %s" %
    #     ('\''+time1+'\'', '\''+retention_type+'\'', len(tmp_uid_ak_retention2), tmp_per2,
    #      len(tmp_uid_ak_retention2), tmp_per2)
    # )

    tmp_per1 = 0
    if len(tmp_uid_ak1) == 0:
        tmp_per1 = 0
    else:
        tmp_per1 = float(len(tmp_uid_ak_retention1)) / float(len(tmp_uid_ak1))
    print time1, retention_type, len(tmp_uid_ak_retention1), tmp_per1
    # query.Query(
    #     " insert INTO ks_data_statistics.ks_retention(statday, retent_type, and_init_num, and_percent) "
    #     "VALUES (%s, %s, %s, %s) on duplicate KEY UPDATE and_init_num = %s, and_percent = %s" %
    #     ('\''+time1+'\'', '\''+retention_type+'\'', len(tmp_uid_ak_retention1), tmp_per1,
    #      len(tmp_uid_ak_retention1), tmp_per1)
    # )
