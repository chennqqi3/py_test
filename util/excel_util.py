# coding=utf-8

import xlwt
import os
from xlwt import Style

__author__ = 'pingli'
'''
   excel 表格导出相关函数
'''

# borders 不能创建太多，xlwt多borders数量有限制，超过了数量后，单元格索引超过borders最大数量则不会显示边界
borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1
borders.bottom_colour = 0x3A


# 创建excel workbook
def create_work_book():
    work_book = xlwt.Workbook(encoding='utf-8')
    return work_book


# 创建sheet表create_sheet
def create_sheet(work_book, sheet_name, head_list):
    sheet = work_book.add_sheet(sheet_name)
    row = 0
    column = 0

    for head in head_list:
        sheet.write(row, column, head)
        column += 1

    return sheet


# 把list列表(列表元素为dict)数据写入sheet表中
def write_sheet_with_list(data_list, sheet, column_key_list, start_row, start_column):
    row = start_row

    for data in data_list:
        column = start_column
        for key in column_key_list:
            sheet.write(row, column, data.get(key))
            column += 1
        row += 1

    return sheet


# 把dict列表(字典存储的元素为dict)数据写入sheet表中
def write_sheet_with_dict(dict_list, sheet, column_key_list, start_row, start_column):
    row = start_row

    for key in sorted(dict_list.keys()):
        data = dict_list.get(key)
        column = start_column
        for column_key in column_key_list:
            sheet.write(row, column, data.get(column_key))
            column += 1
        row += 1

    return sheet


# 向sheet表指定单元格写入内容
def write_cell(sheet, row, column, value, style=None):
    style = set_cell_default_style(style)
    sheet.write(row, column, value, style)


# 合并单元格并且设置单元格的值
def merge_cell(sheet, start_row, end_row, start_column, end_column, value, style=None):
    style = set_cell_default_style(style)
    sheet.write_merge(start_row, end_row, start_column, end_column, value, style)


# 创建一个单元格格式
def create_style(style):
    return xlwt.easyxf(style)


# 设置单元格一些默认样式
def set_cell_default_style(style):
    if not style:
        style = Style.default_style
    style.borders = borders

    return style


# 设置列宽
def set_column_width(sheet, width, column):
    col = sheet.col(column)
    col.width = 256 * width


# 统一设置所有的列宽
def set_all_column_width(sheet, width, column_count):
    for i in range(0, column_count):
        set_column_width(sheet, width, i)


# 保存excel表格文件
def save_excel_file(work_book, file_path):
    if os.path.exists(file_path):
        os.remove(unicode(file_path, 'utf-8'))

    work_book.save(unicode(file_path, encoding='utf-8'))

