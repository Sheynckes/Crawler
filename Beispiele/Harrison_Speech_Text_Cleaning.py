# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 19:07
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : Harrison_Speech.py
# @Software: PyCharm

# 在语言学里有一个模型叫做n-gram， 表示文字或语言中的n个连续的单词组成的序列。
# 下面的代码将输出威廉·亨利·哈里森总统就职演说内容进行以下处理：
# 1. 文本清理，去除单词以外的其他字符；
# 2. 获取2-gram列表，但去除含有stop words的2-gram；
# 3. 按照出现次数对以上2-gram列表进行排序。

from urllib.request import urlopen
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
        cleanText.append(item)
    return cleanText


def get_stop_words():
    url = "https://www.textfixer.com/tutorials/common-english-words.txt"
    stopWords = str(urlopen(url).read(), "utf-8").split(",")
    print(stopWords)
    print(len(stopWords))
    return stopWords


def have_stop_words(nWords, stopWords):
    for word in nWords:
        if word in stopWords:
            return True
    return False


def ngrams(inText, n):
    cleanText = clean_text(inText)
    stopWords = get_stop_words()

    outText = dict()
    for i in range(len(cleanText)-n+1):
        nWords = cleanText[i:i+n]
        if not have_stop_words(nWords, stopWords):
            item = " ".join(nWords)
            if item in outText:
                outText[item] += 1
            else:
                outText[item] = 1
    return outText


n = 2
speech = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), "utf-8")
nPairs = ngrams(speech, n)
nPairsSorted = sorted(nPairs.items(), key=lambda t: t[1], reverse=True)
print(nPairsSorted)
