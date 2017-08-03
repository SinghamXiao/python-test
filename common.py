# coding=utf-8

import codecs
import os

import xlrd

encoding = "utf-8"


# 获取excel数据源
def open_excel(excel_file):
    """获取excel数据源"""
    try:
        data = xlrd.open_workbook(excel_file, formatting_info=True, encoding_override=encoding)
        return data
    except Exception, e:
        print u'excel表格读取失败：%s' % e
        return None


# 保存json到json文件
def save2_json_file(path, filename, data):
    output = codecs.open(os.path.join(path, filename + ".json"), 'w', encoding)
    output.write(data)
    output.close()


# 保存json到json文件
def save2_xml_file(path, filename, doc):
    output = codecs.open(os.path.join(path, filename + ".xml"), 'w', encoding)
    output.write(doc.toprettyxml(encoding=encoding))  # 可以使生成xml有好看的格式，要是不需要，可以使用上一行的代码
    output.close()
