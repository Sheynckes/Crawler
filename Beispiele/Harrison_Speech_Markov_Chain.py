# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 20:22
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : Harrison_Speech_Markov_Chain.py
# @Software: PyCharm

# 下面的代码将根据威廉·亨利·哈里森总统就职演说内容的结构生成任意长度（本例中链长为100）的马尔可夫链组成的句子。

from urllib.request import urlopen
from random import randint, choice


def choose_random_word(wordList):
    words = list(wordList.keys())
    return choice(words)


def build_word_dict(text):
    # 删除换行符和引号
    text = text.replace("\n", " ")
    text = text.replace("\"", "")

    # 保证每个标点符号都和其前面的单词在一起，以保证这些标点符号不会被剔除，可以保留在马尔可夫链中
    punctuation = [',', '.', ';', ":"]
    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ")
    words = text.split()

    # 过滤空单词
    words = [word for word in words if word != ""]

    wordDict = dict()
    for i in range(len(words)-1):
        if words[i] not in wordDict:
            wordDict[words[i]] = dict()
        if words[i+1] not in wordDict[words[i]]:
            wordDict[words[i]][words[i+1]] = 0
        wordDict[words[i]][words[i+1]] += 1
    return wordDict


speech = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), "utf-8")
wordDict = build_word_dict(speech)

# 生成链长为100的马尔可夫链
length = 100
chain = ""
currentWord = "I"

for i in range(0, length):
    chain += currentWord + " "
    currentWord = choose_random_word(wordDict[currentWord])

print(chain)
