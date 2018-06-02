# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 18:27
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : data_cleaning.py
# @Software: PyCharm

# 在语言学里有一个模型叫做n-gram， 表示文字或语言中的n个连续的单词组成的序列。
# 下面的代码将输出维基百科词条『Python programming language』页面中摘要内容的2-gram列表
# 并利用collections.OrderedDict输出该列表中各元素按照出现次数的排序结果

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import string


def clean_text(inText):
    inText = inText.lower()
    inText = re.sub("\n+", " ", inText)
    inText = re.sub("\[[0-9]*\]", "", inText)
    inText = re.sub(" +", " ", inText)
    inText = bytes(inText, "UTF-8")
    inText = inText.decode("ascii", "ignore")
    inText = inText.split(" ")

    cleanText = []
    for item in inText:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() in ("a", "i")):
            cleanText.append(item)
    return cleanText


def ngrams(inText, n):
    cleanText = clean_text(inText)

    outText = dict()
    for i in range(len(cleanText)-n+1):
        item = " ".join(cleanText[i:i+n])
        if item in outText:
            outText[item] += 1
        else:
            outText[item] = 1
    return outText


n = 2
html = urlopen("https://en.wikipedia.org/wiki/Python_(programming_language)")
soup = BeautifulSoup(html, "lxml")
content = soup.find("div", {"id": "mw-content-text"}).get_text()
nPairs = ngrams(content, n)
print(nPairs)
print("%d-grams count is: %d." % (n, len(nPairs)))
nPairsOD = OrderedDict(sorted(nPairs.items(), key=lambda t: t[1], reverse=True))
print(nPairsOD)
