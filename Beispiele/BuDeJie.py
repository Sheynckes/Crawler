# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:16
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : BuDeJie.py
# @Software: PyCharm

# 本程序爬取"www.budejie.com/video/"中的视频，并将视频文件存入budejie文件夹
# 该网页的源代码中，视频地址存放在div标签的data-mp4参数中，可以使用正则表达式将其提取出来


from urllib import request, error
import re

# 定义爬取视频的存储路径
folder = "BuDeJie"
# 定义爬取的页面数量
pages = 100


def get_url_list(page):
    url_page = "http://www.budejie.com/video/%d" % page
    req = request.Request(url_page)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0')
    res = request.urlopen(req)
    html = res.read().decode('utf-8')

    reg = r'data-mp4="(.*?)">'
    url_list = re.findall(reg, html)

    for url_mp4 in url_list:
        name = url_mp4.split('/')[-1]
        try:
            request.urlretrieve(url_mp4, '%s/%s' % (folder, name))
        except error.HTTPError:
            print(url_mp4)


for page in range(pages):
    get_url_list(page + 1)
