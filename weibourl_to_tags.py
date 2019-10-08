# -*- coding: utf-8 -*-
import log_version_rom
import json
import urllib.request
import re
import datetime

def remove_4char(string):
    try:
        # python UCS-4 build的处理方式
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        # python UCS-2 build的处理方式
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    resovle_value = highpoints.sub('', string)
    return resovle_value


def parse(mblogid):
    url = 'https://m.weibo.cn/statuses/show?id=' + mblogid
    proxy_addr = log_version_rom.get_proxy_addr()
    try:
        html = log_version_rom.use_proxy(url, proxy_addr)
        if html == -1:
            return
        content = json.loads(html)
        data = content.get('data')
        values = {
            'microBlogName':data.get('user').get('screen_name'),
            'ifDav': 'Yes',
            'microBlogClass': str(data.get('user').get('urank')),
            'fansNumber': str(data.get('user').get('followers_count')),
            'likeNumber': str(data.get('user').get('follow_count')),
            'allNumber': str(data.get('user').get('statuses_count')),
            'wsummary': re.sub('<[^>]*>','',data.get('status_title')).replace('#', ''),
            'contents': re.sub('<[^>]*>','',data.get('text')).replace('#', ''),
            'captionType': None,
            'publishTime': datetime.datetime.strptime(data.get('created_at'), '%a %b %d %H:%M:%S %z %Y').strftime("%Y-%m-%d %H:%M:%S"),
            'forwardNumber': str(data.get('reposts_count')),
            'commentNumber': str(data.get('comments_count')),
            'praiseNumber': str(data.get('attitudes_count')),
            'articleNumber': "-1",
            'microBlogFrom': '新浪微博',
            'microBlogLabel': '新闻大V',
            'weiboId': data.get('id'),
            'weiboUrl': url,
            'picUrl': [],
            'wsmallPic': data.get('thumbnail_pic'),
            'wtfskey': [],
            'wpicWidth': "0",
            'wpicHeight': "0",
            'picSet': data.get('pics'),
            #'commentSet':[],
            'consensLabel': None,
            'isAccident': None,
            'accountId': str(data.get('user').get('id')),
            'fromAccountId': None,
            'orginWebsiteName': None,
            'orignUrl': None,
            'tags': None,
            'idTag': None
        }

        values['wsummary'] = remove_4char(values['wsummary'])
        if data.get('retweeted_status') != None:
            values['fromAccountId'] = str(data.get('retweeted_status').get('user').get('id'))
            values['orginWebsiteName'] = data.get('retweeted_status').get('source')
            values['orignUrl'] = 'https://m.weibo.cn/status/'+data.get('retweeted_status').get('id')
        else:
            values['fromAccountId'] = str(data.get('user').get('id'))
            values['orginWebsiteName'] = '新浪微博'
            values['orignUrl'] = url

        # try:
        #     comment_url = 'https://m.weibo.cn/api/comments/show?id=' + mblogid
        #     i = 0
        #     while True:
        #         comment_contents = log_version_rom.use_proxy(comment_url+'&page='+str(i), log_version_rom.get_proxy_addr())
        #         if comment_contents != -1:
        #             if json.loads(comment_contents).get('data') != None:
        #                 values['commentSet'].extend(json.loads(comment_contents).get('data').get('data'))
        #             else:
        #                 for term in values['commentSet']:
        #                     term['text'] = remove_4char(re.sub('<[^>]*>', '', term['text']).replace("#", ''))
        #                     term['id'] = str(term['id'])
        #                     term['user']['id'] = str(term['user']['id'])
        #                     term['user']['verified_type'] = str(term['user']['verified_type'])
        #                     term['user']["mbtype"] = str(term['user']["mbtype"])
        #                     term['like_counts'] = str(term['like_counts'])
        #                 break
        #         i += 1
        # except Exception as e:
        #     print(e)
        #     pass

        my_headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

        if values['picSet'] != None:
            for pic in values['picSet']:
                try:
                    values['picUrl'].append(pic['url'])
                    wtfskey_api = 'http://data.mgt.chinaso365.com/cp-center/tfs/getkey?imgurl=' + pic['url']
                    pic_response = urllib.request.urlopen(wtfskey_api,timeout=5)
                    values['wtfskey'].append(json.loads(pic_response)['tfskey'][21:])
                except Exception as e:
                    print(e)
                    pass

        for item, value in values.items():
            if value == None:
                values[item] = "null"


        try:
            resjson = {
                "resourceFk": "dab19e82e1f9a681ee73346d3e7a575e",
                "submitWay":"4",
                "partnerId":"1000",
                "specials": values
            }
            url = 'http://data.mgt.chinaso365.com/datasrv/2.0/resources/01347/submit?resjson='+json.dumps(resjson)
            print(url)
            response = log_version_rom.use_proxy(url, log_version_rom.get_proxy_addr())
            print(response)
        except Exception as e:
            print(e)
            pass

    except Exception as e:
        print(e)
        pass



if __name__=='__main__':
    #id = '4278830035979631'
    id = '4280397757562777'
    parse(id)