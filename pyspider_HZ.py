from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
import time
import redis
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
import xmltodict
'''惠州'''

class Handler(My):
    name = "HZ"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/ghjsj/ph_xzyjs/index.html', callback=self.index_page)
        # self.crawl('http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/ghjsj/ph_ydghxkz/index.html', callback=self.index_page)
        # self.crawl('http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/ghjsj/ph_gcghxkz/index.html', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        t = soup('script', {'language':'JavaScript'})
        l = t[1].get_text().split('\'')
        x = l[13]
        d = xmltodict.parse(x)
        k = d['xml']['RECS']['INFO']
        links = []
        for i in k:
            links.append(i['InfoURL'])
        url = "http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/"
        for i in links:
            link = url + i
            # print(link)
            self.crawl(link, callback=self.content_page)
            time.sleep(0.1)  