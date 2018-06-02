# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:22
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : QQ_Video.py
# @Software: PyCharm

# 网上的代码，未运行过

import re
import urllib
from bs4 import BeautifulSoup
import string, time
import pymongo

NUM = 0  # 全局变量,电影数量
m_type = u''  # 全局变量,电影类型
m_site = u'qq'  # 全局变量,电影网站


# 根据指定的URL获取网页内容
def gethtml(url):
    req = urllib.Request(url)
    response = urllib.urlopen(req)
    html = response.read()
    return html


# 从电影分类列表页面获取电影分类
def gettags(html):
    global m_type
    soup = BeautifulSoup(html)  # 过滤出分类内容
    # print soup
    # <ul class="clearfix _group" gname="mi_type" gtype="1">
    tags_all = soup.find_all('ul', {'class': 'clearfix _group', 'gname': 'mi_type'})
    # print len(tags_all), tags_all
    # print str(tags_all[1]).replace('\n', '')

    # <a _hot="tag.sub" class="_gtag _hotkey" href="http://v.qq.com/list/1_0_-1_-1_1_0_0_20_0_-1_0.html"title="动作" tvalue="0">动作</a>
    re_tags = r'<a _hot=\"tag\.sub\" class=\"_gtag _hotkey\" href=\"(.+?)\" title=\"(.+?)\" tvalue=\"(.+?)\">.+?</a>'
    p = re.compile(re_tags, re.DOTALL)

    tags = p.findall(str(tags_all[0]))
    if tags:
        tags_url = {}
        # print tags
        for tag in tags:
            tag_url = tag[0].decode('utf-8')
            # print tag_url
            m_type = tag[1].decode('utf-8')
            tags_url[m_type] = tag_url

    else:
        print("Not Find")
    return tags_url


# 获取每个分类的页数
def get_pages(tag_url):
    tag_html = gethtml(tag_url)
    # div class="paginator
    soup = BeautifulSoup(tag_html)  # 过滤出标记页面的html
    # print soup
    # <div class="mod_pagenav" id="pager">
    div_page = soup.find_all('div', {'class': 'mod_pagenav', 'id': 'pager'})
    # print div_page #len(div_page), div_page[0]

    # <a class="c_txt6" href="http://v.qq.com/list/1_2_-1_-1_1_0_24_20_0_-1_0.html" title="25"><span>25</span></a>
    re_pages = r'<a class=.+?><span>(.+?)</span></a>'
    p = re.compile(re_pages, re.DOTALL)
    pages = p.findall(str(div_page[0]))
    # print pages
    if len(pages) > 1:
        return pages[-2]
    else:
        return 1


def getmovielist(html):
    soup = BeautifulSoup(html)

    # <ul class="mod_list_pic_130">
    divs = soup.find_all('ul', {'class': 'mod_list_pic_130'})
    # print divs
    for div_html in divs:
        div_html = str(div_html).replace('\n', '')
        # print div_html
        getmovie(div_html)


def getmovie(html):
    global NUM
    global m_type
    global m_site

    re_movie = r'<li><a class=\"mod_poster_130\" href=\"(.+?)\" target=\"_blank\" title=\"(.+?)\"><img.+?</li>'
    p = re.compile(re_movie, re.DOTALL)
    movies = p.findall(html)
    if movies:
        conn = pymongo.Connection('localhost', 27017)
        movie_db = conn.dianying
        playlinks = movie_db.playlinks
        # print movies
        for movie in movies:
            # print movie
            NUM += 1
            print("%s : %d" % ("=" * 70, NUM))
            values = dict(
                movie_title=movie[1],
                movie_url=movie[0],
                movie_site=m_site,
                movie_type=m_type
            )
            print(values)
            playlinks.insert(values)
            print("_" * 70)
            NUM += 1
            print("%s : %d" % ("=" * 70, NUM))

    # else:
    #   print "Not Find"


def getmovieinfo(url):
    html = gethtml(url)
    soup = BeautifulSoup(html)

    # pack pack_album album_cover
    divs = soup.find_all('div', {'class': 'pack pack_album album_cover'})
    # print divs[0]

    # <a href="http://www.tudou.com/albumplay/9NyofXc_lHI/32JqhiKJykI.html" target="new" title="《血滴子》独家纪录片" wl="1"> </a>
    re_info = r'<a href=\"(.+?)\" target=\"new\" title=\"(.+?)\" wl=\".+?\"> </a>'
    p_info = re.compile(re_info, re.DOTALL)
    m_info = p_info.findall(str(divs[0]))
    if m_info:
        return m_info
    else:
        print("Not find movie info")

    return m_info


def insertdb(movieinfo):
    global conn
    movie_db = conn.dianying_at
    movies = movie_db.movies
    movies.insert(movieinfo)


if __name__ == "__main__":
    global conn

    tags_url = "http://v.qq.com/list/1_-1_-1_-1_1_0_0_20_0_-1_0.html"
    # print tags_url
    tags_html = gethtml(tags_url)
    # print tags_html
    tag_urls = gettags(tags_html)
    # print tag_urls

    for url in tag_urls.items():
        print(str(url[1]).encode('utf-8'))  # ,url[0]
        maxpage = int(get_pages(str(url[1]).encode('utf-8')))
        print(maxpage)

        for x in range(0, maxpage):
            # http://v.qq.com/list/1_0_-1_-1_1_0_0_20_0_-1_0.html
            m_url = str(url[1]).replace('0_20_0_-1_0.html', '')
            movie_url = "%s%d_20_0_-1_0.html" % (m_url, x)
            print(movie_url)
            movie_html = gethtml(movie_url.encode('utf-8'))
            # print movie_html
            getmovielist(movie_html)
            time.sleep(0.1)