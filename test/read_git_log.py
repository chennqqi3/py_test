# coding=utf-8

import datetime
import sys
from util import excel_util
from dateutil.parser import *

reload(sys)
sys.setdefaultencoding("utf-8")

file_path = r'd:/git_log.xls'

if __name__ == '__main__':
    with open("D:\\idea\\ks_ndb_api\\log.txt") as file_obj:
        arr = []
        obj = {}
        for line in file_obj:
            line = line.strip()
            if line.find('commit ') != -1:
                if obj is not None:
                    arr.append(obj)
                obj = {}
            elif line.find('Author: ') != -1:
                obj.setdefault("author", line.replace('Author: ', ''))
            elif line.find('Date:   ') != -1:
                obj.setdefault('date', parse(line.replace('Date:   ', '')).date())
            elif len(line) != 0 and line.find('Merge:') == -1:
                obj.setdefault('message', line)

        head_list = ['author', 'date', 'message']
    column_key_list = ['author', 'date', 'message']
    work_book = excel_util.create_work_book()

    consultation_sheet = excel_util.create_sheet(work_book, 'git log', head_list)

    excel_util.write_sheet_with_list(arr, consultation_sheet, column_key_list, 1, 0)

    excel_util.save_excel_file(work_book, file_path)