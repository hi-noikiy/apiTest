__author__ = 'lily'
# -*- coding: utf-8 -*-
import xlrd
import os
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

def getExcel(homeExcel):
    try:
        wb = xlrd.open_workbook(homeExcel)
        table = wb.sheet_by_index(0)  # 第一个表
        nrows = table.nrows
        colnameindex = 1
        colnames = table.row_values(colnameindex)
        result = {}
        list = []
        for rownum in range(2, nrows):
            row = table.row_values(rownum)
            tmp = {}
            if row:
                for i in range(len(colnames)-0):
                    tmp[colnames[i]] = row[i]
            list.append(tmp)
        return list

    except FileNotFoundError:
        print(u"找不到文件")



