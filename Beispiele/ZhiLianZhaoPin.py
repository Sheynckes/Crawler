# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:25
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : ZhiLianZhaoPin.py
# @Software: PyCharm

# 使用并发爬取智联招聘

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re

url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=python&sm=0&p=1'
wbdata = requests.get(url).content
soup = BeautifulSoup(wbdata, 'lxml')

items = soup.select("div#newlist_list_content_table > table")
# 每页职位信息数量，打印结果为60
count = len(items) - 1
print(count)
# 搜索到的总职位数量
job_count = re.findall(r"共<em>(.*?)</em>个职位满足条件", str(soup))[0]
# 搜索结果的页数，打印结果为484
pages = (int(job_count) // count) + 1
print(pages)


def get_zhaopin(page):
    url = "https://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=python&sm=0&p=%d" % page
    print("第%d页" % page)
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata, 'lxml')

    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")
    for name, salary, location, time in zip(job_name, salarys, locations, times):
        data = {
            'name': name.get_text(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'time': time.get_text()
        }
        print(data)


if __name__ == '__main__':
    # 实例化一个进程池，设置进程为2
    pool = Pool(processes=2)
    # 调用进程池的map_async()方法，接收一个函数(爬虫函数)和一个列表(url列表)
    pool.map_async(get_zhaopin, range(1, pages + 1))
    pool.close()
    pool.join()
