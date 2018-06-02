# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 19:25
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : wiki_six_degree_1.py
# @Software: PyCharm

# 从维基百科的一个词条页面出发，获取该页面中所有指向其他词条页面的链接；
# 从上述链接中随机选取一个链接，并保存该链接地址（以集合类型保存，以避免链接重复）；
# 从这个随机选取出的链接出发，重复上述过程。

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random


random.seed(datetime.datetime.now())

urls = set()


def get_links(articleUrl):
    html = urlopen("https://en.wikipedia.org" + articleUrl)
    soup = BeautifulSoup(html, "lxml")
    # 获取指向词条页面的链接，该链接有以下三个共同点：
    # (1) 它们都在id是bodyContent的div标签里；
    # (2) URL链接不包括冒号；
    # (3) URL链接都以/wiki/开头。
    return soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))


url = "/wiki/Kevin_Bacon"
links = get_links(url)

while len(links) > 0:
    articleUrl = links[random.randint(0, len(links) - 1)].attrs["href"]
    if articleUrl not in urls:
        urls.add(articleUrl)
        print(articleUrl)
    links = get_links(articleUrl)
