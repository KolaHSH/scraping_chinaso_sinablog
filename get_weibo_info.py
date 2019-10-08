# -*- coding: utf-8 -*-

import datetime

def get_time(publish_time, crawl_time):
    if (publish_time.find('刚刚') != -1):
        publish_time = crawl_time
    elif (publish_time.find('分钟') != -1):
        delta = int(publish_time[0:publish_time.find('分钟')])
        timedelta = datetime.timedelta(minutes=-delta)
        crawl_time_std = datetime.datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
        publish_time_std = crawl_time_std + timedelta
        publish_time = publish_time_std.strftime('%Y-%m-%d %H:%M:%S')
    elif (publish_time.find('小时') != -1):
        delta = int(publish_time[0:publish_time.find('小时')])
        timedelta = datetime.timedelta(hours=-delta)
        crawl_time_std = datetime.datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
        publish_time_std = crawl_time_std + timedelta
        publish_time = publish_time_std.strftime('%Y-%m-%d %H:%M:%S')
    elif (publish_time.find('昨天') != -1):
        time_str = publish_time[3:]
        timedelta = datetime.timedelta(days=-1)
        crawl_time_std = datetime.datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
        publish_time_std = crawl_time_std + timedelta
        publish_time1 = publish_time_std.strftime('%Y-%m-%d %H:%M:%S')
        publish_time = publish_time1[0:11] + time_str + ':00'
    elif(publish_time[0] == '2' and publish_time[1] == '0' and publish_time[4] == '-' and publish_time[7] == '-'):
        publish_time = publish_time + crawl_time[10:]
    else:
        time_str = publish_time
        publish_time = crawl_time[0:5] + time_str + crawl_time[10:]
    return publish_time

def get_weibo_data(line):
    line_list = line.split('&&&&')
    # [日志信息/爬取时间， 微博账号，账号id， 微博id， 微博地址， 发布时间， 微博内容，点赞数，评论数，转发数，图片集, 转自微博用户id，转自微博id]
    #crawl_time = line[line.find('[') + 1:line.find('[') + 20]
    crawl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    account_id = line_list[2]
    weibo_id = line_list[3]
    contents = line_list[6]
    weibo_url = line_list[4]
    zan = line_list[7]
    comment = line_list[8]
    transfer = line_list[9]
    if line.find('无配图') == -1:
        pics = line_list[10]
    else:
        pics = None
    from_account_id = line_list[11] if (line_list[11] != '-1') else None
    from_weibo_id = line_list[12] if (line_list[12] != '-1') else None
    publish_time = get_time(line_list[5], crawl_time)
    return weibo_id, weibo_url, contents, zan, transfer, comment, pics, publish_time, crawl_time, account_id, from_account_id, from_weibo_id

if __name__ == '__main__':
    with  open('output.log', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            get_weibo_data(line)
            line = f.readline()

