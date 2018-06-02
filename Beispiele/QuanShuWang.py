# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:23
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : QuanShuWang.py
# @Software: PyCharm

# 本程序爬取"www.quanshuwang.com/"中的书籍信息，并将书籍的分类名称、书名、封面图片、简介、状态（是否连载）、作者等信息写入数据库；

from urllib import request
from bs4 import BeautifulSoup
import re


first_page = 1


def get_last_page(url):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0')
    res = request.urlopen(req)
    html = res.read().decode('gbk')

    reg = r'<a href="http://www.quanshuwang.com/list/(.*?).html" class="last">'
    last = re.findall(reg, html)[0].split('_')[-1]
    return int(last)


def get_sort_dict():
    sort_dict = {}
    url_home = "http://www.quanshuwang.com/"
    req = request.Request(url_home)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0')
    res = request.urlopen(req)
    html = res.read().decode('gbk')
    soup = BeautifulSoup(html, 'lxml')
    sort_list = soup.select("ul.channel-nav-list > li > a")

    for sort_id, sort in enumerate(sort_list):
        sort_id += 1
        sort_name = sort.get_text()
        sort_dict[sort_id] = sort_name

    return sort_dict


def get_book_info(book_url):
    req = request.Request(book_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0')
    res = request.urlopen(req)
    html = res.read().decode('gbk')

    # 获取书名
    reg_title = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    title = re.findall(reg_title, html)[0]

    # 获取简介, re.S表示匹配字符串时包含换行符
    reg_description = r'<meta property="og:description" content="(.*?)"/>'
    description = re.findall(reg_description, html, re.S)[0][24:]

    # 获取作者
    reg_author = r'<meta property="og:novel:author" content="(.*?)"/>'
    author = re.findall(reg_author, html)[0]

    # 获取状态
    reg_status = r'<meta property="og:novel:status" content="(.*?)"/>'
    status = re.findall(reg_status, html)[0]

    # 获取章节地址
    reg_chapters = r'<a href="(.*?)" class="reader"'
    chapters = re.findall(reg_chapters, html)[0]

    return title, author, description, status, chapters


def get_books(sort_id, page):
    url_page = "http://www.quanshuwang.com/list/%d_%d.html" % (sort_id, page)
    req = request.Request(url_page)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0')
    res = request.urlopen(req)
    html = res.read().decode('gbk')

    reg = r'<a target="_blank" href="(.*?)" class="l mr10">'
    url_list = re.findall(reg, html)
    for url in url_list:
        return get_book_info(url)


sort_dict = get_sort_dict()

for sort_id, sort_name in sort_dict.items():
    url_sort = "http://www.quanshuwang.com/list/%d_%d.html" % (sort_id, first_page)
    last_page = get_last_page(url_sort)
    for page in range(first_page, last_page + 1):
        title, author, description, status, chapters = get_books(sort_id, page)
        print("Sort Name: ", sort_name)
        print("Title: ", title)
        print("Author: ", author)
        print("Description: ", description)
        print("Status: ", status)
        print("Chapters: ", chapters)
        print()
