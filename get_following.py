# -*- coding: utf-8 -*-
#将关注列表保存到txt中，格式为 name:id + '\n'

import requests
import json

def get(containerid, pagenum, file_name):
    for i in range(0,pagenum):
        url = "https://m.weibo.cn/api/container/getSecond?containerid=" + str(containerid) + "_-_FOLLOWERS&page=" + str(i)
        req = requests.get(url)
        data = json.loads(req.text)
        content = data.get("data").get("cards")
        for j in content:
            followingId = j['user']['id']
            followingName = j['user']['screen_name']
            #print(followingName + ":" + str(followingId))
            with open(file_name, 'a', encoding='utf-8') as fh:
                fh.write(followingName + ":" + str(followingId) + "\n")


if __name__ == '__main__':
    get(1005056650444073, 18, "following_list.txt")
