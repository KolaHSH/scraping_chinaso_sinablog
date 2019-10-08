# -*- coding: utf-8 -*-

import datetime
import time

def get_time():


def get_weibo_data(line):
    crawl_time = line[line.find('[') + 1:line.find('[') + 20]
    weibo_id = line[line.find('微博id') + 5:line.find('微博id') + 21]
    contents = line[line.find('微博内容') + 5:line.find('点赞数') - 1]
    zan = line[line.find('点赞数') + 4:line.find('评论数')]
    comment = line[line.find('评论数') + 4:line.find('转发数')]
    if line.find('无配图') == -1:
        transfer = line[line.find('转发数') + 4:line.find('图片集')]
        pics = line[line.find('图片集') + 4:]
    else:
        transfer = line[line.find('转发数') + 4:line.find('无配图')]
        pics = None
    # print((weibo_id, contents, zan, transfer, comment, crawl_time, pics))
    publish_l = line.find('发布时间')
    publish_r = line.find('微博内容')
    if (line.find('分钟', publish_l, publish_r) != -1):
        delta = int(line[publish_l + 5:line.find('分钟', publish_l, publish_r)])
        timedelta = datetime.timedelta(minutes=-delta)
        crawl_time_std = datetime.datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
        publish_time_std = crawl_time_std + timedelta
        publish_time = publish_time_std.strftime('%Y-%m-%d %H:%M:%S')
    elif (line.find('小时', publish_l, publish_r) != -1):
        delta = int(line[publish_l + 5:line.find('小时', publish_l, publish_r)])
        timedelta = datetime.timedelta(hours=-delta)
        crawl_time_std = datetime.datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
        publish_time_std = crawl_time_std + timedelta
        publish_time = publish_time_std.strftime('%Y-%m-%d %H:%M:%S')
    elif (line.find('昨天', publish_l, publish_r) != -1):
        time_str = line[line.find('发布时间', publish_l, publish_r) + 8:line.find('发布时间', publish_l, publish_r) + 13]
        timedelta = datetime.timedelta(days=-1)
        crawl_time_std = datetime.datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
        publish_time_std = crawl_time_std + timedelta
        publish_time1 = publish_time_std.strftime('%Y-%m-%d %H:%M:%S')
        publish_time = publish_time1[0:11] + time_str + ':00'
    else:
        time_str = line[line.find('发布时间', publish_l, publish_r) + 5:line.find('发布时间', publish_l, publish_r) + 10]
        publish_time = crawl_time[0:5] + time_str + crawl_time[10:]
        # print(publish_time)
    return weibo_id, contents, zan, transfer, comment, pics, publish_time, crawl_time

if __name__ == '__main__':
    with  open('output.log', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            print(get_weibo_data(line))
            line = f.readline()
            time.sleep(1)

