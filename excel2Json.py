#!/usr/bin/env python
# coding=utf-8

import codecs
import json
import os
import sys

import xlrd

VALUE = "value"


# 把excel表格中指定sheet转为json
def excel2json(excel_file_path):
    # 打开excel文件
    excel = read_excel(excel_file_path)
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
            result = {"worksheet": worksheet, "rows": nrows, VALUE: []}  # 定义json对象

            # 遍历所有行，将excel转化为json对象
            for i in range(nrows):
                if i == 0:
                    continue
                tmp = {}
                # 遍历当前行所有列
                for j in range(ncols):
                    # 获取当前列中文标题
                    title_de = str(row_0[j]).decode('unicode_escape')
                    title_cn = title_de.split("'")[1]
                    # 获取单元格的值
                    tmp[title_cn] = sheet.row_values(i)[j]
                result[VALUE].append(tmp)

            save_file(os.getcwd(), worksheet,
                      json.dumps(result, indent=4).decode('unicode_escape'))


# 获取excel数据源
def read_excel(excel_file_path):
    """获取excel数据源"""
    try:
        data = xlrd.open_workbook(excel_file_path)
        return data
    except Exception, e:
        print u'excel表格读取失败：%s' % e
        return None


# 保存json到json文件
def save_file(file_path, file_name, data):
    output = codecs.open(file_path + "/" + file_name + ".json", 'w', "utf-8")
    output.write(data)
    output.close()


if __name__ == '__main__':
    print("Start Transfer...")

    sys_argv = sys.argv
    if len(sys.argv) < 2:
        print("usage: python excel2Json.py filename.xls")
        sys.exit(1)

    excel_file = sys.argv[1]
    print("excel file: " + excel_file)
    excel2json(excel_file)
    print ("Success Transfer...")
