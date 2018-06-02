# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 20:34
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : wiki_six_degree_3.py
# @Software: PyCharm

# 把维基百科中与"https://en.wikipedia.org/wiki/Kevin_Bacon"页面的链接数不超过6个的词条页面储存起来

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv


def write_csv(f="", t="", n=None):
    try:
        csvFile = open("wiki_six_degree_3.csv", "a+")
        writer = csv.writer(csvFile)
        writer.writerow((f, t, n))
    finally:
        csvFile.close()


def get_links(articleUrl, recursionNumber):
    global urls

    if recursionNumber == 6:
        return

    html = urlopen("https://en.wikipedia.org" + articleUrl)
    soup = BeautifulSoup(html, "lxml")

    # 获取指向词条页面的链接，该链接有以下三个共同点：
    # (1) 它们都在id是bodyContent的div标签里；
    # (2) URL链接不包括冒号；
    # (3) URL链接都以/wiki/开头。
    for link in soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if "href" in link.attrs:
            newArticleUrl = link.attrs["href"]
            if newArticleUrl not in urls:
                write_csv(articleUrl, newArticleUrl, recursionNumber)
                urls.add(newArticleUrl)
                print(newArticleUrl)
                get_links(newArticleUrl, recursionNumber+1)


write_csv("FromUrl", "ToUrl", "LinkNumber")
url = "/wiki/Kevin_Bacon"
urls = set([url])
get_links(url, 1)
