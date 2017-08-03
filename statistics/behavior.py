# coding=utf-8
from util import db_util

query = db_util.get_query()


# APP行为
def behavior():
        query.call_proc('ksexpt.proc_call_behavior')