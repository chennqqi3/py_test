# coding=utf-8
from util import db_util

query = db_util.get_query()


def base(path, activate_file_list, stat_file_list, register_file_list):
    all_activation_device(path, stat_file_list)
    plant_activation_device(path, stat_file_list)
    all_activation_user(path, stat_file_list)
    plant_activation_user(path, stat_file_list)
    all_active_user(path, activate_file_list)
    plant_active_user(path, activate_file_list)
    avg_duration_tot(path, stat_file_list)
    avg_duration_plant(path, stat_file_list)
    register_num_plant(path, register_file_list)


# 设备活跃数
def all_activation_device(path, stat_file_list):
    file_object = open(path+'stat.log')

    dic = {}
    active = {}

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
                device_id = arr[4]
                time_device_key = time + 's' + device_id
                dic.setdefault(time_device_key, 0)
                dic[time_device_key] += 1

        for time_device_key, visit_num in dic.items():
            date = time_device_key[0:10]
            active.setdefault(date, 0)
            active[date] += 1

        for date, count in active.items():
            query.Query(
                " insert INTO ks_data_statistics.ks_base(statday, active_tot_num) "
                "VALUES (%s, %s) on duplicate KEY UPDATE active_tot_num = %s" %
                ('\''+date+'\'', count, count)
            )

    finally:
        file_object.close()


# 平台设备活跃数
def plant_activation_device(path, stat_file_list):
    file_object = ''

    active = {}
    plant = {}

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
                if arr[1] == 'null':
                    continue
                ak = arr[1][2:3]
                device_id = arr[4]
                time_plant_device_key = time + ak + 's' + device_id
                plant.setdefault(time_plant_device_key, 0)
                plant[time_plant_device_key] += 1

        for date_device_key, visit_num in plant.items():
            date = date_device_key[0:11]
            active.setdefault(date, 0)
            active[date] += 1

        for date, count in active.items():
            if date[10:11] == '1':
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, active_and_num) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE active_and_num = %s" %
                    ('\''+date[0:10]+'\'', count, count)
                )
            elif date[10:11] == '2':
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, active_ios_num) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE active_ios_num = %s" %
                    ('\''+date[0:10]+'\'', count, count)
                )

    finally:
        file_object.close()


# 用户活跃数
def all_activation_user(path, stat_file_list):
    file_object = open(path+'stat.log')

    dic = {}
    active = {}

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
                time_uid_key = time + 's' + uid
                dic.setdefault(time_uid_key, 0)
                dic[time_uid_key] += 1

        for time_uid_key, visit_num in dic.items():
            date = time_uid_key[0:10]
            active.setdefault(date, 0)
            active[date] += 1

        for date, count in active.items():
            query.Query(
                " insert INTO ks_data_statistics.ks_base(statday, active_tot_user_num) "
                "VALUES (%s, %s) on duplicate KEY UPDATE active_tot_user_num = %s" %
                ('\''+date+'\'', count, count)
            )

    finally:
        file_object.close()


# 平台用户活跃数
def plant_activation_user(path, stat_file_list):
    file_object = ''

    active = {}
    plant = {}

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
                if arr[1] == 'null':
                    continue
                ak = arr[1][2:3]
                uid = arr[3]
                time_plant_uid_key = time + ak + 's' + uid
                plant.setdefault(time_plant_uid_key, 0)
                plant[time_plant_uid_key] += 1

        for date_uid_key, visit_num in plant.items():
            date = date_uid_key[0:11]
            active.setdefault(date, 0)
            active[date] += 1

        for date, count in active.items():
            if date[10:11] == '1':
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, active_and_user_num) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE active_and_user_num = %s" %
                    ('\''+date[0:10]+'\'', count, count)
                )
            elif date[10:11] == '2':
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, active_ios_user_num) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE active_ios_user_num = %s" %
                    ('\''+date[0:10]+'\'', count, count)
                )

    finally:
        file_object.close()


# 用户激活数
def all_active_user(path, activate_file_list):
    file_object = ''

    dic = {}
    active = {}

    try:
        for f in activate_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                if arr == '' or len(arr) < 3:
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                time = arr[0][0:10]
                device_id = arr[2]
                time_uid_key = time + 's' + device_id
                dic.setdefault(time_uid_key, 0)
                dic[time_uid_key] += 1

        for date_uid_key, visit_num in dic.items():
            date = date_uid_key[0:10]
            active.setdefault(date, 0)
            active[date] += 1
        for date, count in active.items():
            query.Query(
                " insert INTO ks_data_statistics.ks_base(statday, init_tot_num) "
                "VALUES (%s, %s) on duplicate KEY UPDATE init_tot_num = %s" %
                ('\''+date+'\'', count, count)
            )

    finally:
        file_object.close()


# 平台用户激活数
def plant_active_user(path, activate_file_list):
    file_object = ''

    active = {}
    plant = {}

    try:
        for f in activate_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                if arr == '' or len(arr) < 3:
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                time = arr[0][0:10]
                ak = arr[1][17:18]
                if arr[1] == 'null':
                    continue
                device_id = arr[2]
                time_plant_uid_key = time + ak + 's' + device_id
                plant.setdefault(time_plant_uid_key, 0)
                plant[time_plant_uid_key] += 1

        for date_uid_key, visit_num in plant.items():
            date = date_uid_key[0:11]
            active.setdefault(date, 0)
            active[date] += 1

        for date, count in active.items():
            if date[10:11] == '1':
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, init_and_num) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE init_and_num = %s" %
                    ('\''+date[0:10]+'\'', count, count)
                )
            elif date[10:11] == '2':
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, init_ios_num) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE init_ios_num = %s" %
                    ('\''+date[0:10]+'\'', count, count)
                )

    finally:
        file_object.close()


# 用户在线时长
def avg_duration_tot(path, stat_file_list):
    file_object = ''

    uid_total_time = {}
    uid_pre_time = {}

    try:
        for f in stat_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                time = arr[0][0:10]
                detail_time = arr[0][11:19]
                uid_pre_time.setdefault(time, 0)
                uid_total_time.setdefault(time, 0)
                if line.find("ks_web/api/notice") != -1:
                    continue

                if uid_pre_time[time] == 0:
                    uid_pre_time[time] = detail_time
                else:
                    total_time = (int(detail_time[0:2]) - int(uid_pre_time[time][0:2])) * 3600 + (int(
                        detail_time[3:5]) - int(uid_pre_time[time][3:5])) * 60 + (
                                        int(detail_time[6:8]) - int(uid_pre_time[time][6:8]))
                    if 30 * 60 > total_time > 0:
                        uid_total_time[time] = int(uid_total_time[time]) + int(total_time)
                    uid_pre_time[time] = detail_time

        for date, count in uid_total_time.items():
            query.Query(
                " insert INTO ks_data_statistics.ks_base(statday, avgduration_tot) "
                "VALUES (%s, %s) on duplicate KEY UPDATE avgduration_tot = %s" %
                ('\''+date+'\'', count, count)
            )

    finally:
        file_object.close()


# 平台用户在线时长
def avg_duration_plant(path, stat_file_list):
    file_object = ''

    uid_total_time = {}
    uid_pre_time = {}
    android_total_time = {}
    ios_total_time = {}

    try:
        for f in stat_file_list:
            file_object = open(path+f)

            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                time = arr[0][0:10]
                detail_time = arr[0][11:19]
                ak = arr[1][2:3]
                if arr[1] == 'null':
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                ak_uid = ak + "s" + time
                uid_pre_time.setdefault(ak_uid, 0)
                uid_total_time.setdefault(ak_uid, 0)

                if uid_pre_time[ak_uid] == 0:
                    uid_pre_time[ak_uid] = detail_time
                else:
                    total_time = (int(detail_time[0:2]) - int(uid_pre_time[ak_uid][0:2])) * 3600 + (int(
                        detail_time[3:5]) - int(uid_pre_time[ak_uid][3:5])) * 60 + (
                                    int(detail_time[6:8]) - int(uid_pre_time[ak_uid][6:8]))
                    if 30 * 60 > total_time > 0:
                        uid_total_time[ak_uid] = int(uid_total_time[ak_uid]) + int(total_time)
                    uid_pre_time[ak_uid] = detail_time

        for ak_uid_key, visit_num in uid_total_time.items():
            ak, userid = ak_uid_key.split('s')
            if ak == '1':
                android_total_time[userid] = visit_num
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, avgduration_and) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE avgduration_and = %s" %
                    ('\''+userid+'\'', visit_num, visit_num)
                )

            elif ak == '2':
                ios_total_time[userid] = visit_num
                query.Query(
                    " insert INTO ks_data_statistics.ks_base(statday, avgduration_ios) "
                    "VALUES (%s, %s) on duplicate KEY UPDATE avgduration_ios = %s" %
                    ('\''+userid+'\'', visit_num, visit_num)
                )

    finally:
        file_object.close()


def register_num_plant(path, register_file_list):
    date_plant_uid_arr = []
    and_date = {}
    ios_date = {}
    user_id_dic = {}

    for f in register_file_list:
        with open(path+f) as file_object:
            for line in file_object:
                line = line.strip()
                arr = line.split(',')
                time = arr[0][0:10]
                if arr[1] == 'null':
                    continue
                if line.find("ks_web/api/notice") != -1:
                    continue
                ak = arr[1].split(':')[2][2:3]
                uid = arr[2].split(':')[1]
                if time in user_id_dic.keys():
                    uid_dic = user_id_dic[time]
                    if len(uid_dic) > 0 and uid in uid_dic:
                        date_plant_uid_arr.append(time+'s'+ak+'s'+uid)
                else:
                    uid_dic = is_today_register(time)
                    user_id_dic.setdefault(time, [])
                    user_id_dic[time] = uid_dic
                    if len(uid_dic) > 0 and uid in uid_dic:
                        date_plant_uid_arr.append(time+'s'+ak+'s'+uid)

    date_plant_uid_arr = set(date_plant_uid_arr)

    for date_plant_uid in date_plant_uid_arr:
        date, ak, uid = date_plant_uid.split('s')
        if ak == '1':
            and_date.setdefault(date, 0)
            and_date[date] += 1
        elif ak == '2':
            ios_date.setdefault(date, 0)
            ios_date[date] += 1

    if len(and_date) > 0:
        for date, c in and_date.items():
            query.Query(
                " insert INTO ks_data_statistics.ks_base(statday, register_and_num) "
                "VALUES (%s, %s) on duplicate KEY UPDATE register_and_num = %s" %
                ('\''+date+'\'', c, c)
            )

    if len(ios_date) > 0:
        for date, c in ios_date.items():
            query.Query(
                " insert INTO ks_data_statistics.ks_base(statday, register_ios_num) "
                "VALUES (%s, %s) on duplicate KEY UPDATE register_ios_num = %s" %
                ('\''+date+'\'', c, c)
            )


# 查询今天注册的uid
def is_today_register(statday):
    user_id_dic = []
    query.Query("select uid from ksexpt.ks_user WHERE left(register_time,10) = '"+statday+"'")
    for row in query.record:
        user_id = row['uid']
        user_id_dic.append(str(user_id))

    return user_id_dic
