# coding: utf-8

from util import db_util
import re
from pinyin import pinyin

query = db_util.get_product_query()


wd = '李王张刘陈杨黄赵周吴徐孙朱马胡郭林何高梁'
wd +='郑罗宋谢唐韩曹许邓萧冯曾程蔡彭潘袁于董余'
wd +='苏叶吕魏蒋田杜丁沈姜范江傅钟卢汪戴崔任陆'
wd +='廖姚方金邱夏谭韦贾邹石熊孟秦阎薛侯雷白龙'
wd +='段郝孔邵史毛常万顾赖武康贺严尹钱施牛洪龚'
wd +='汤陶黎温莫易樊乔文安殷颜庄章鲁倪庞邢俞翟'
wd +='蓝聂齐向申葛岳伍覃骆关焦柳欧祝纪尚毕耿芦'


def non_comp_rule(keyword):
    wd1 = str.decode(wd, "utf-8")
    # keyword = str.decode(keyword, "utf-8")
    if len(keyword) < 2 or re.match("\d+$", keyword):
        return 1
    if len(keyword) in (2, 3) and keyword[0:1] in wd1:
        return 1
    if keyword.find(u"公司") != -1:
        return 2


def trans_pinyin(keyword):
    return keyword


def query_kw() :
    kw_list = list()
    query.Query("SELECT * FROM capvision_fun.clst_search_kw_add_task WHERE sch_type = 0 ")
    for row in  query.record:
        kw = dict(id=row['id'], keywords=row['keywords'])

        kw['sch_type'] = non_comp_rule(kw['keywords'])
        if kw['sch_type']==1:
            print kw['keywords'], len(kw["keywords"]),kw['sch_type']
            kw_list.append(kw)
            query.Query("update capvision_fun.clst_search_kw_add_task set sch_type = 1 where id = %d ;" % kw["id"])
        elif kw['sch_type']==2:
            query.Query("update capvision_fun.clst_search_kw_add_task set sch_type = 2 where id = %d ;" % kw["id"])
    print len(kw_list)


def pinyin_trans():
    query.Query("SELECT * FROM capvision_fun.cslt_search_ana_add_task")
    wd1 = str.decode(wd, "utf-8")
    for row in query.record:
        keywords = row['keywords']
        if len(keywords) in (2, 3) and keywords[0:1] in wd1:
            print keywords
            query.Query("update capvision_fun.cslt_search_ana_add_task set kw_tag = 'xm' WHERE  id = %s" % ( row["id"]))
        elif keywords.find(u"公司") != -1:
            # print keywords
            query.Query("update capvision_fun.cslt_search_ana_add_task set kw_tag = 'gs' WHERE  id = %s" % ( row["id"]))


if __name__ == '__main__':
    # query_kw()
    pinyin_trans()



