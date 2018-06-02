# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:22
# @Author  : SHeynckes
# @Email   : shenghai@ymail.com
# @File    : QQ_Zone.py
# @Software: PyCharm

# 使用Selenium抓取QQ空间好友说说

from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 使用selenium的webdriver实例化一个浏览器对象，这里使用Chrome
driver = webdriver.Chrome()
driver.maximize_window()


# 登录QQ空间
def get_shuoshuo(qq, password):
    # 使用get()方法打开待抓取的URL
    driver.get("http://user.qzone.qq.com/{}/311".format(qq))

    # 等待5秒后，判断页面是否需要登录，通过查找页面是否有相应的div的id来判断：
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    # 如果页面存在登录的div，则模拟登录：
    if a == True:
        # 切换到登录的frame
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        # 选择用户名框
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(qq)
        # 选择密码框
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(password)
        # 点击登录按钮
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)

    # 判断好友空间是否设置了权限，通过判断是否存在元素ID：QM_OwnerInfo_Icon
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    # 如果有权限能够访问到说说页面，那么定位元素和数据，并解析：
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for con, sti in zip(content, stime):
            data = {
                'time': sti.text,
                'shuos': con.text
            }
            print(data)
        # 除了在Selenium中解析数据，还可以将当前页面保存为源码，再使用BeautifulSoup来解析：
        pages = driver.page_source
        soup = BeautifulSoup(pages, 'lxml')

    # 最后，尝试使用get_cookies()获取Cookie：
    cookie_ = driver.get_cookies()
    cookie_dict = []
    for c in cookie_:
        ck = "{0}={1}".format(c['name'], c['value'])
        cookie_dict.append(ck)

    print('Cookies: ', '; '.join(cookie_dict))
    print("==========Done==========")

    driver.close()
    driver.quit()


if __name__ == "__main__":
    qq = '549920536'
    password = 'leon@qq'
    get_shuoshuo(qq, password)
