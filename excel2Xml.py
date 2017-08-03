#!/usr/bin/env python
# coding=utf-8

import os
import sys
import xml.dom.minidom

from common import open_excel
from common import save2_xml_file

info = "info"


def excel2xml(excel_file):
    excel = open_excel(excel_file)
    worksheets = excel.sheet_names()
    for worksheet in worksheets:
        index = worksheets.index(worksheet)
        print ('process sheet %s: %s' % (index, worksheet))
        sheet = excel.sheet_by_index(index)
        nrows = sheet.nrows  # 行号
        ncols = sheet.ncols  # 列号

        # 创建dom文档对象
        doc = xml.dom.minidom.Document()
        # 创建根元素
        info_element = doc.createElement(info)
        # 将根元素添加到文档中区
        doc.appendChild(info_element)

        for nrow in range(1, nrows):
            # 创建元素
            item = doc.createElement('item')
            for ncol in range(0, ncols):
                key = u"%s" % sheet.cell(0, ncol).value
                value = sheet.cell(nrow, ncol).value
                if isinstance(value, float):
                    value = '%0d' % value
                print type(key), type(value)
                # 将数据都作为xml中元素的属性，属性名就是第一行的值，属性值就是某一行某一列的值
                item.setAttribute(key.encode('utf-8'), value.encode('utf-8'))

            # 将此元素作为根元素的子节点
            info_element.appendChild(item)

        save2_xml_file(os.getcwd(), worksheet, doc)


if __name__ == '__main__':
    print("Transfer *.xls To *.xml...")
    sys_argv = sys.argv
    if len(sys.argv) < 2:
        print("usage: python excel2Xml.py filename.xls")
        sys.exit(1)

    excel_file = sys.argv[1]
    print("excel file: " + excel_file)
    excel2xml(excel_file)
    print ("Transfer Success...")
