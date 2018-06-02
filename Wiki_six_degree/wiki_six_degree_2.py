# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 20:15
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : wiki_six_degree_3.py
# @Software: PyCharm

# 从维基百科的一个词条页面出发，获取该页面中的标题、第一段文字，并存入csv文件；
# 遍历所有指向其他词条页面的链接，重复上述过程。

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv


def write_csv(t="", c=""):
    try:
        csvFile = open("wiki_six_degree_2.csv", "a+")
        writer = csv.writer(csvFile)
        writer.writerow((t, c))
    finally:
        csvFile.close()


def get_links(articleUrl):
    global urls

    html = urlopen("https://en.wikipedia.org" + articleUrl)
    soup = BeautifulSoup(html, "lxml")

    try:
        title = soup.h1.get_text()
        content = soup.find(id="mw-content-text").findAll("p")[0]
        write_csv(title, content)
    except AttributeError:
        print("The page lacks some attributes. No worries.")

    # 获取指向词条页面的链接，该链接有以下三个共同点：
    # (1) 它们都在id是bodyContent的div标签里；
    # (2) URL链接不包括冒号；
    # (3) URL链接都以/wiki/开头。
    for link in soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if "href" in link.attrs:
            articleUrl = link.attrs["href"]
            if articleUrl not in urls:
                urls.add(articleUrl)
                print(articleUrl)
                get_links(articleUrl)


write_csv("Title", "Content")
url = "/wiki/Kevin_Bacon"
urls = set([url])
get_links(url)
