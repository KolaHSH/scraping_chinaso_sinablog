# -*- coding: utf-8 -*-

import urllib.request
import json
import random
import requests
import bs4
from bs4 import BeautifulSoup
import re
import proxy_list

my_headers = {
   'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36,    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36,    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14,   Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
}



#设置某个用户的id
id = '1947072791'

#从免费代理网站上获取免费代理ip
def get_proxy_addr():
    proxy_url = 'http://www.xicidaili.com/nn/'
    html = requests.get(proxy_url, headers = my_headers)
    soup = BeautifulSoup(html.text, 'lxml')
    ips = soup.find('tr', attrs={'class': re.compile("(odd)|()")})
    proxy_addr = ips.find_all('td')
    return(proxy_addr[1].string+ ':'+ proxy_addr[2].string)


#使用代理和模拟浏览器打开页面
def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent",random.choice(my_headers['User-Agent']))
    proxy = urllib.request.ProxyHandler({'http':proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8','ignore')
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
def get_userInfo(id):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=100505' + id
    data = use_proxy(url, get_proxy_addr())
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

def get_weibo(id, file):
    i = 1
    while True:
        #个人主页
        url = 'https://m.weibo.cn/p/100505' + id
        #个人主页中包含微博正文的部分
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(url, get_proxy_addr()) + '&page=' + str(i)
        try:
            data = use_proxy(weibo_url, get_proxy_addr())
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if(len(cards)>0):
                for j in range(len(cards)):
                    print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    if(cards[j].get('card_type')==9):
                        mblog = cards[j].get('mblog')
                        attitudes_count = mblog.get('attitudes_count')
                        comments_count = mblog.get('comments_count')
                        created_at = mblog.get('created_at')
                        reposts_count = mblog.get('reposts_count')
                        scheme = cards[j].get('scheme')
                        text = mblog.get('text')
                        pics = mblog.get('pics')
                        if (len(pics) > 0):
                            pics_url = list()
                            for pic in pics:
                                pics_url.append(pic['url'])
                        print("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
                        print("微博地址：" + str(scheme))
                        print("发布时间：" + str(created_at))
                        print("微博内容：" + str(text))
                        print("点赞数：" + str(attitudes_count))
                        print("评论数：" + str(comments_count))
                        print("转发数：" + str(reposts_count))
                        print("图片集：" + ','.join(pics_url))
                        with open(file, 'a', encoding='utf-8') as fh:
                            fh.write("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
                            fh.write("微博地址：" + str(scheme) + "\n" + "发布时间：" + str(created_at) + "\n" + "微博内容：" + text + "\n" +"点赞数：" + str(attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(reposts_count) + "\n" + "图片集：" + ','.join(pics_url) + "\n")
                i += 1
            else:
                break
        except Exception as e:
            print(e)
            pass



if __name__ == '__main__':
    file = id+'.txt'
    get_userInfo(id)
    get_weibo(id, file)