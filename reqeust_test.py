# -*- coding: utf-8 -*-

import urllib
import json
import log_version_rom

resjson = {'resourceFk': 'dab19e82e1f9a681ee73346d3e7a575e', 'submitWay': '4', 'partnerId': '01347', 'specials': {'microBlogName': '哲easy唐禹哲國際後援', 'ifDav': 'Yes', 'microBlogClass': 40, 'fansNumber': '15578', 'likeNumber': '126', 'allNumber': '8337', 'wsummary': '🏙🏙🏙好久不見 唐禹哲HOTHEART...', 'contents': '唐禹哲  #唐禹哲0902生日快乐#  #唐禹哲平妖传之天书奇谭#  #唐禹哲山月不知心底事#  好久不見！日日思念！不過後天就可以見你啦😃', 'captionType': None, 'publishTime': 'Thu Aug 30 21:33:59 +0800 2018', 'forwardNumber': '1', 'commentNumber': '2', 'praiseNumber': '46', 'articleNumber': None, 'microBlogFrom': '新浪微博', 'microBlogLabel': '新闻大V', 'weiboId': '4278830035979631', 'weiboUrl': 'https://m.weibo.cn/statuses/show?id=4278830035979631', 'picUrl': [], 'wsmallPic': None, 'wtfskey': [], 'wpicWidth': None, 'wpicHeight': None, 'picSet': None, 'commentSet': [{'id': 4279038439141232, 'created_at': '5小时前', 'source': '', 'user': {'id': 5655833755, 'screen_name': '吴永伟爱生活', 'profile_image_url': 'https://tvax2.sinaimg.cn/crop.0.0.1002.1002.180/006aLiJ5ly8fpdvrvahqjj30ru0ru0ul.jpg', 'verified': False, 'verified_type': -1, 'mbtype': 0, 'profile_url': 'https://m.weibo.cn/u/5655833755?uid=5655833755', 'remark': '', 'following': False, 'follow_me': False}, 'text': '项链好显眼', 'like_counts': 0, 'liked': False}], 'consensLabel': None, 'isAccident': None, 'accountId': '2040787977', 'fromAccountId': 1634785555, 'orginWebsiteName': '唐禹哲超话', 'orignUrl': None, 'tags': None, 'idTag': None, 'orginUrl': 'https://m.weibo.cn/status/4278829386622902'}}

url = 'http://data.mgt.chinaso365.com/datasrv/2.0/resources/01108/submit?resjson='+json.dumps(resjson)

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36,    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36,    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14,   Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"}

try:
    response = log_version_rom.use_proxy(url, log_version_rom.get_proxy_addr())
    print(response)
    print(response.read())
except Exception as e:
    print(e)