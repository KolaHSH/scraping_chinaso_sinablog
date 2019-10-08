# -*- coding: utf-8 -*-

def crawl_write(cards, i, j, file):
    if (cards[j].get('card_type') == 9):
        ispic = 0
        mblog = cards[j].get('mblog')
        attitudes_count = mblog.get('attitudes_count')
        comments_count = mblog.get('comments_count')
        created_at = mblog.get('created_at')
        reposts_count = mblog.get('reposts_count')
        scheme = cards[j].get('scheme')
        text = mblog.get('text')
        weibo_id = mblog.get('id')
        pics = mblog.get('pics')
        pics_url = list()
        # print("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
        # print("微博id：" + str(weibo_id))
        # print("微博地址：" + str(scheme))
        # print("发布时间：" + str(created_at))
        # print("微博内容：" + str(text))
        # print("点赞数：" + str(attitudes_count))
        # print("评论数：" + str(comments_count))
        # print("转发数：" + str(reposts_count))
        if (pics != None):
            ispic = 1
            for pic in pics:
                pics_url.append(pic['url'])
            print("图片集：" + ','.join(pics_url))
        else:
            print("无配图")
        with open(file, 'a', encoding='utf-8') as fh:
            fh.write("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
            if (ispic):
                fh.write("微博id：" + str(weibo_id) + "\n" + "微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                    created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(attitudes_count) + "\n" + "评论数：" + str(
                    comments_count) + "\n" + "转发数：" + str(reposts_count) + "\n" + "图片集：" + ','.join(pics_url) + "\n")
            else:
                fh.write("微博id：" + str(weibo_id) + "\n" + "微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                    created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(
                    attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(
                    reposts_count) + "\n" + "无配图" + "\n")

def crawl_log(cards, j, name, logger):
    if (cards[j].get('card_type') == 9):
        ispic = 0
        mblog = cards[j].get('mblog')
        attitudes_count = mblog.get('attitudes_count')
        comments_count = mblog.get('comments_count')
        created_at = mblog.get('created_at')
        reposts_count = mblog.get('reposts_count')
        scheme = cards[j].get('scheme')
        text = mblog.get('text')
        text_replace = text.replace('\n', '&&&')
        weibo_id = mblog.get('id')
        pics = mblog.get('pics')
        pics_url = list()
        # print("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
        # print("微博id：" + str(weibo_id))
        # print("微博地址：" + str(scheme))
        # print("发布时间：" + str(created_at))
        # print("微博内容：" + str(text))
        # print("点赞数：" + str(attitudes_count))
        # print("评论数：" + str(comments_count))
        # print("转发数：" + str(reposts_count))
        if (pics != None):
            ispic = 1
            for pic in pics:
                pics_url.append(pic['url'])
        else:
            pass
        if (ispic):
            logger.info("微博昵称：" + name + "微博id：" + str(weibo_id) + "微博地址：" + str(scheme) + "发布时间：" + str(created_at) + "微博内容：" + text_replace + "点赞数：" + str(attitudes_count) + "评论数：" + str(comments_count) + "转发数：" + str(reposts_count) + "图片集：" + ','.join(pics_url))
        else:
            logger.info("微博昵称：" + name + "微博id：" + str(weibo_id) + "微博地址：" + str(scheme) + "发布时间：" + str(created_at) + "微博内容：" + text_replace + "点赞数：" + str(attitudes_count) + "评论数：" + str(comments_count) + "转发数：" + str(reposts_count) + "无配图")



