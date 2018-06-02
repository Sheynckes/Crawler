# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:20
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : Postcode.py
# @Software: PyCharm

# 本程序从http://www.ip138.com/post中获取全国所有县市区的邮政编码和长途区号
# 目前，以下代码仅完成提取各省名称和链接地址的工作

import requests
from xml.parsers.expat import ParserCreate


class DefaultSaxHandler(object):
    def __init__(self, provinces):
        self.provinces = provinces

    def start_element(self, name, attrs):
        if name != 'map':
            name = attrs['title']  # province name
            number = attrs['href']  # link location
            self.provinces.append((name, number))

    def end_element(self, name):
        pass

    def char_data(self, text):
        pass


def get_provinces(url):
    content = requests.get(url).content.decode('gb2312')
    start = content.find('<map name=\"map_86" id=\"map_86\">')
    end = content.find('</map>')
    content = content[start: end + len('</map>')].strip()
    print(content)

    provinces_list = []
    # 定义处理器
    handler = DefaultSaxHandler(provinces_list)
    # 定义解析器
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    # 解析content内容
    parser.Parse(content)
    return provinces_list


provinces = get_provinces('http://www.ip138.com/post')
print(provinces)
