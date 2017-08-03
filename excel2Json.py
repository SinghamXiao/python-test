#!/usr/bin/env python
# coding=utf-8

import json
import os
import sys

from common import open_excel
from common import save2_json_file

info = "info"


# 把excel表格中指定sheet转为json
def excel2json(excel_file):
    # 打开excel文件
    excel = open_excel(excel_file)
    if excel is not None:
        # 抓取所有sheet页的名称
        worksheets = excel.sheet_names()

        for worksheet in worksheets:
            index = worksheets.index(worksheet)
            print ('process sheet %s: %s' % (index, worksheet))
            sheet = excel.sheet_by_index(index)
            row_0 = sheet.row(0)  # 第一行是表单标题
            nrows = sheet.nrows  # 行号
            ncols = sheet.ncols  # 列号
            result = {"worksheet": worksheet, "rows": nrows, info: []}  # 定义json对象

            # 遍历所有行，将excel转化为json对象
            for row in range(nrows):
                if row == 0:
                    continue
                tmp = {}
                # 遍历当前行所有列
                for col in range(ncols):
                    # 获取当前列中文标题
                    title_de = str(row_0[col]).decode('unicode_escape')
                    title_cn = title_de.split("'")[1]
                    # 获取单元格的值
                    tmp[title_cn] = sheet.row_values(row)[col]
                result[info].append(tmp)

            save2_json_file(os.getcwd(), worksheet, json.dumps(result, indent=4).decode('unicode_escape'))


if __name__ == '__main__':
    print("Transfer *.xls To *.json...")
    sys_argv = sys.argv
    if len(sys.argv) < 2:
        print("usage: python excel2Json.py filename.xls")
        sys.exit(1)

    excel_file = sys.argv[1]
    print("excel file: " + excel_file)
    excel2json(excel_file)
    print ("Transfer Success...")
