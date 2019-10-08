# -*- coding: utf-8 -*-

import urllib.request
import json
import random
import time
import requests
from bs4 import BeautifulSoup
import re
import write_file
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

global key_value



#提供代理ip和端口的网站
proxy_url = 'http://www.xicidaili.com/nn/'

#从免费代理网站上获取免费代理ip
def get_proxy_addr():
    try:
        my_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36,    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36,    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14,   Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
        }
        html = requests.get(proxy_url, headers = my_headers)
        soup = BeautifulSoup(html.text, 'lxml')
        ips = soup.find('tr', attrs={'class': re.compile("(odd)|()")})
        if ips is None:
            return "122.241.72.191:808"
        else:
            proxy_addr = ips.find_all('td')
            return (proxy_addr[1].string + ':' + proxy_addr[2].string)
    except Exception as e:
        return "122.241.72.191:808"

#使用代理和模拟浏览器打开页面
def use_proxy(url, proxy_addr):
    try:
        my_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36,    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36,    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14,   Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
        }
        req = urllib.request.Request(url)
        req.add_header("User-Agent", random.choice(my_headers['User-Agent']))
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
        return data
    except Exception as e:
        print(e)
        return -1

#爬取微博api请求时需要的containerid
def get_containerid(url, proxy_addr):
    data = use_proxy(url, proxy_addr)
    if(data == -1):
        return -1
    else:
        content = json.loads(data).get('data')
        if content is None:
            return -1
        for data in content.get('tabsInfo').get('tabs'):
            if (data['tab_type'] == 'weibo'):
                containerid = data['containerid']
        return containerid

#通过id找到该人对应微博及每一页api请求内容
def get_userInfo(id, proxy_addr):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=100505' + id
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    description = content.get('userInfo').get('description')
    profile_url = content.get('userInfo').get('profile_url')
    verified = content.get('userInfo').get('verified')
    guanzhu = content.get('userInfo').get('follow_count')
    name = content.get('userInfo').get('screen_name')
    fensi = content.get('userInfo').get('followers_count')
    gender = content.get('userInfo').get('gender')
    urank = content.get('userInfo').get('urank')
    print("微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "\n" + "是否认证：" +     str(verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(fensi) + "\n" + "性别："     + gender + "\n" + "微博等级：" + str(urank) + "\n")

def get_weibo(name, id, logger_weibo, proxy_addr):
    i = 1
    flag = 1
    while i <= 5 and flag:
        # 个人主页
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        # 个人主页中包含微博正文的部分
        containerid = get_containerid(url, proxy_addr)
        if containerid == -1:
            continue
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + containerid + '&page=' + str(i)
        data = use_proxy(weibo_url, proxy_addr)
        if(data == -1):
            continue
        else:
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if (i == 1):
                lastid = cards[0].get('mblog').get('id')
            check_id = key_value[id]
            if (len(cards) > 0 and flag):
                for j in range(len(cards)):
                    # print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    if (cards[j].get('mblog').get('id') != check_id):
                        write_file.crawl_log(cards, j, name, logger_weibo)
                    else:
                        flag = 0
                        break
                #print(i)
                i += 1
            else:
                flag = 0
    key_value[id] = lastid

def create_log():
    logger = logging.getLogger('weibo_spider')
    formatter = logging.Formatter(
        '[%(asctime)s] [%(threadName)s:%(thread)d] [%(levelname)s]: %(message)s')
    file_handler = TimedRotatingFileHandler('output.log', when='midnight',encoding='utf-8')
    file_handler.setFormatter(formatter)
    #console_handler = logging.StreamHandler(sys.stdout)
    #console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == '__main__':
    global key_value
    key_value = {}
    following_file = 'following_list.txt'
    #following_file = sys.argv[1]
    with open(following_file, mode='r',encoding='utf-8', errors='ignore') as f:
        data = f.readlines()
    logger_weibo = create_log()
    for item in data:
        sp = item.split(":")
        id = sp[1][:-1]
        key_value[id] = 0
    cnt = 1
    for item in data:
        # time.sleep(5)
        sp = item.split(":")
        name = sp[0]
        id = sp[1][:-1]
        print(str(cnt) + "." + name)
        proxy_addr = get_proxy_addr()
        # get_userInfo(id, proxy_addr)
        get_weibo(name, id, logger_weibo, proxy_addr)
        cnt = cnt + 1
