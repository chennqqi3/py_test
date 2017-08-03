# coding=utf-8

import xlrd
import xlwt
from datetime import date,datetime
from util import excel_util
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


total_file_path = r'E:\total_data.xls'


def read_excel(file_path):
    tot_list = []
    # 打开文件
    workbook = xlrd.open_workbook(file_path)
    if len(workbook.sheet_names()) < 1:
        return
    # for i in range(0, len(workbook.sheet_names())):
    for i in range(0, 1):
        sheet = workbook.sheet_by_name(workbook.sheet_names()[i])
        # print sheet.name,sheet.nrows,sheet.ncols
        if sheet.nrows < 1 or sheet.ncols < 1:
            continue
        for j in range(13, sheet.nrows):
            # print sheet.row_values(i)
            # value = ""
            if sheet.cell(j, 1).ctype != 3:
                break
            if sheet.cell(10, 2).value is None or sheet.cell(10, 2).value == '':
                print 'empty name:', file_path
            obj = {}
            for k in range(0, sheet.ncols):
                # value += str(sheet.cell(j, k).value) + " "
                # ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                # ['name', 'date', 'type', 'currency', 'amount', 'rate', 'rmb_amount', 'purpose']
                if k == 0:
                    obj.setdefault('name', '')
                    obj['name'] = sheet.cell(10, 2).value.encode('utf-8')
                if k == 1:
                    obj.setdefault('date', '')
                    obj['date'] = "-".join([str(i) for i in xlrd.xldate_as_tuple(sheet.cell(j, k).value, 0)[0:3]])
                if k == 2:
                    obj.setdefault('type', '')
                    obj['type'] = sheet.cell(j, k).value.encode('utf-8')
                if k == 3:
                    obj.setdefault('currency', '')
                    obj['currency'] = sheet.cell(j, k).value.encode('utf-8')
                if k == 4:
                    obj.setdefault('amount', '')
                    obj['amount'] = sheet.cell(j, k).value
                if k == 5:
                    obj.setdefault('rate', '')
                    obj['rate'] = sheet.cell(j, k).value
                if k == 6:
                    obj.setdefault('rmb_amount', '')
                    obj['rmb_amount'] = sheet.cell(j, k).value
                if k == 7:
                    obj.setdefault('purpose', '')
                    obj['purpose'] = sheet.cell(j, k).value.encode('utf-8')
            tot_list.append(obj)

    return tot_list


if __name__ == '__main__':
    list_file = os.listdir(r"E:\fin_excel")
    # print len(list_file)
    tot_list = []
    # i = 0
    for file_path in list_file:
        # i += 1
        # if i > 20:
        #     break
        if file_path.find('.xls') == -1 and file_path.find('.xlsx') == -1:
            continue
        print 'path:', file_path
        try:
            tmp_list = read_excel(r"E:\fin_excel\\" + file_path)
            if len(tmp_list) > 0:
                for obj in tmp_list:
                    tot_list.append(obj)
        except:
            print 'except file:', file_path

    head_list = ['Name', 'Date', '*Expense Type', 'Currency', 'Amount', 'Ex. Rate', 'RMB Amount', 'Business Purpose']
    column_key_list = ['name', 'date', 'type', 'currency', 'amount', 'rate', 'rmb_amount', 'purpose']
    work_book = excel_util.create_work_book()

    consultation_sheet = excel_util.create_sheet(work_book, u'汇总', head_list)

    excel_util.write_sheet_with_list(tot_list, consultation_sheet, column_key_list, 1, 0)

    excel_util.save_excel_file(work_book, total_file_path)

    print u'存放路径：', 'E:\total_data.xls'
