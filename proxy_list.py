# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re
import json
import time

def get_proxy_list(url):
    page = urllib.request.urlopen(url).read()
    html = json.loads(page)
    #print(html['domain'])
    #print(html['port'][0])
    return(html['domain']+':'+str(html['port'][0]))


if __name__ == '__main__':
    time_last = int(time.time())
    url = 'http://183.129.207.77:88/open?user_name=hysvcdfyt34563&timestamp=' + str(time_last) + '1531904010&md5=b231bfafcf0eaca44d2af69f1c05d447&number=1&pattern=json'
    proxy = get_proxy_list(url)
    print(proxy)