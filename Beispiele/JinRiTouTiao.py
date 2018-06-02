# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:18
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : JinRiTouTiao.py
# @Software: PyCharm

# 本程序使用JS爬取今日头条，并将爬取的数据存入MongoDB

import requests
import json
import pymongo

# 建立一个MongoDB的连接
conn = pymongo.MongoClient(host='localhost', port=27017)
toutiao = conn['toutiao']
newsdata = toutiao['news']

# 对数据接口进行http请求
url = 'http://www.toutiao.com/api/pc/focus/'
wbdata = requests.get(url).text

# 对HTTP响应的数据JSON化，并索引到新闻数据的位置
data = json.loads(wbdata)
news = data['data']['pc_feed_focus']

# 对索引出来的JSON数据进行遍历和提取
for n in news:
    title = n['title']
    img_url = n['image_url']
    url = n['media_url']
    data = {
        'title': title,
        'img_url': img_url,
        'url':url
    }
    newsdata.insert_one(data)

for i in newsdata.find():
    print(i)
