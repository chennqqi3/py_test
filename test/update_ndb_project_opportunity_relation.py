#!/usr/bin/python
# coding=utf-8

import MySQLdb


def update():
    conn = MySQLdb.connect(host='192.168.50.11', user='admin', passwd='admin1234', db="vesta", charset="UTF8")
    cur=conn.cursor()
    cur.execute("""select a.project_id,a.ksh_status,1 from
  (SELECT db_project_id as project_id,status as ksh_status FROM vesta.vesta_project_opportunity where ifnull(db_project_id,0)<>0 order by status
  )a
  group by a.project_id
  """)
    fet=cur.fetchall()
    vp=list(fet)

    conn1 = MySQLdb.connect(host='192.168.5.241', user='admin', passwd='admin4321', db="ndb", charset="UTF8")
    cur1=conn1.cursor()
    cur1.execute("truncate table ndb_project_opportunity_relation")
    conn1.commit()
    cur1.executemany("insert into ndb_project_opportunity_relation(project_id,ksh_status,running_state) values(%s,%s,%s)",vp)
    print('finished insert data into ndb_project_opportunity_relation table ')
    conn1.commit()
    conn1.close()
    cur1.close()
    conn.close()
    cur.close()


def main(count):
    conn = MySQLdb.connect(host='192.168.5.87', user='admin', passwd='admin1234', db="ksexpt", charset="UTF8")
    cur = conn.cursor()
    t_list = []
    t_list.append('select * from ks_user limit ')
    t_list.append(str(count))
    sql = ''.join(t_list)
    # 'select * from ks_user limit ', count
    cur.execute(sql)
    fet = cur.fetchall()
    print str(fet).decode('utf8')

if __name__ == '__main__':
    # main(1)
    t = u'\u4eff\u5236\u836f\u884c\u4e1a\u6807\u6746\u5404\u6709\u7279\u70b9\uff0c\u5236\u5242\u51fa\u53e3\u672a\u6765\u4ecd\u662f\u7a81\u7834'
    print t
    # t = (58, 50)
    # print t[1]