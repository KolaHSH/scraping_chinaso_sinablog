# -*- coding: utf-8 -*-

import urllib.request
import json
import random
import time
import requests
from bs4 import BeautifulSoup
import re
#import proxy_list
import write_file
import os


my_headers = {
   'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36,    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36,    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14,   Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
}

#提供代理ip和端口的网站
proxy_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='

#设置某个用户的id
#id = '1740116803'

#从免费代理网站上获取免费代理ip
def get_proxy_addr():
    # html = requests.get(proxy_url, headers = my_headers)
    # soup = BeautifulSoup(html.text, 'lxml')
    # ips = soup.find('tr', attrs={'class': re.compile("(odd)|()")})
    # proxy_addr = ips.find_all('td')
    # return(proxy_addr[1].string+ ':'+ proxy_addr[2].string)
    url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    html = requests.get(url, headers=my_headers)
    text = BeautifulSoup(html.text, 'lxml')
    ip = text.find_all('p')
    return(ip[0].string)

#使用代理和模拟浏览器打开页面
def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent",random.choice(my_headers['User-Agent']))
    proxy = urllib.request.ProxyHandler({'http':proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req, timeout=3).read().decode('utf-8','ignore')
    return data

#爬取微博api请求时需要的containerid
def get_containerid(url, proxy_addr):
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data['tab_type'] == 'weibo'):
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

#找到个人微博主页第一页中上次更新到的最后一条微博
def find_last(name, cards):
    if not os.path.exists(name+'.txt'):
        return -1
    with open(name+'.txt', "r", encoding='utf-8' ) as f:
        line = f.readline()
        line = f.readline()
        id = line[5:-1]
    if(len(cards)>0):
        for j in range(len(cards)):
            if (cards[j].get('card_type') == 9):
                mblog = cards[j].get('mblog')
                newid = mblog['id']
                if(newid == id):
                    return j
    return -1

def get_weibo(name, id, file, proxy_addr):
    i = 1
    # 个人主页
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
    # 个人主页中包含微博正文的部分
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(
        url, proxy_addr) + '&page=' + str(i)
    try:
        data = use_proxy(weibo_url, proxy_addr)
        content = json.loads(data).get('data')
        cards = content.get('cards')
        last = find_last(name, cards)
        # 发现第一页上有上次爬取过的信息，故只需更新第一页的内容即可
        if(last == 0):
            pass
        elif (last > 0) :
            print("以下是%s在%s的更新：" %(name, time.asctime(time.localtime(time.time()))))
            for j in range(last):
                write_file.crawl_write(cards, i, j, 'new.txt')
            with open(name+'.txt', 'r+', encoding='utf-8') as f:
                content = f.read()
                f.seek(0,0)
                with open('new.txt', 'r', encoding='utf-8') as f_add:
                    content_add = f_add.read()
                    f.write(content_add+"以上是%s在%s的更新：" %(name, time.asctime(time.localtime(time.time())))+'\n'+content)
            os.remove('new.txt')
        # 在第一页上没有发现爬取过的信息，按从未爬取过处理
        else:
            while (i < 10):
                # 个人主页
                url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
                # 个人主页中包含微博正文的部分
                weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(url, proxy_addr) + '&page=' + str(i)
                try:
                    data = use_proxy(weibo_url, proxy_addr)
                    content = json.loads(data).get('data')
                    cards = content.get('cards')
                    if (len(cards) > 0):
                        for j in range(len(cards)):
                            print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                            write_file.crawl_write(cards, i, j, file)
                        print(i)
                        i += 1
                    else:
                        break
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    following_file = 'following_list.txt'
    with open(following_file, mode='r',encoding='utf-8', errors='ignore') as f:
        data = f.readlines()
    while True:
        for item in data:
            #time.sleep(2)
            sp = item.split(":")
            name = sp[0]
            id = sp[1][:-1]
            file = name + ".txt"
            print(name)
            proxy_addr = get_proxy_addr()
            #get_userInfo(id, proxy_addr)
            get_weibo(name, id, file, proxy_addr)