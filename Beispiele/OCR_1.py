# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 21:05
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : OCR_1.py
# @Software: PyCharm

from urllib.request import urlretrieve
from selenium import webdriver
import time
import subprocess


url = "http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200"
# 创建新的selenium driver
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

# 单击图书预览按钮
driver.find_element_by_id("sitbLogoImg").click()
# 等待页面完成加载
time.sleep(5)

imageSet = set()

# 当向右箭头可以点击时，开始翻页
while "pointer" in driver.find_element_by_id("siteReaderRightPageTurner").get_attribute("style"):
    time.sleep(2)
    # 获取已加载的新页面（一次可以加载多个页面，但是重复的页面不再存入集合中）
    pages = driver.find_element_by_xpath("//div[@class='pageImage']/div/img")
    for page in pages:
        image = page.get_attribute("src")
        imageSet.add(image)

driver.quit()

# 用Tesseract处理已经收集的图片URL链接
for image in sorted(imageSet):
    urlretrieve(image, "page.jpg")
    p = subprocess.Popen(["tesseract", "page.jpg", "page"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    f = open("page.txt", "r")
    print(f.read())
