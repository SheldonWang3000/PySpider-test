from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
import redis
from urllib.parse import urljoin 
from urllib.parse import urlparse
from urllib.parse import urlunparse
'''汕头'''

class Handler(My):
    name = "ST"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.stghj.gov.cn/Category_218/Index.aspx', callback=self.index_page)
        self.crawl('http://www.stghj.gov.cn/Category_217/Index.aspx', callback=self.index_page)
        self.crawl('http://www.stghj.gov.cn/Category_221/Index.aspx', callback=self.index_page)
        self.crawl('http://www.stghj.gov.cn/Category_295/Index.aspx', callback=self.index_page)
        self.crawl('http://www.stghj.gov.cn/Category_292/Index.aspx', callback=self.index_page)
        self.crawl('http://www.stghj.gov.cn/Category_276/Index.aspx', callback=self.index_page)
        self.crawl('http://www.stghj.gov.cn/Category_279/Index.aspx', callback=self.index_page)

    def index_page(self, response):
        soup = BeautifulSoup(response.text)

        t = soup('div', {'class':'pagecss'})[0].find_all('a')[-1]['href']
        try:
            page_count = int(t.split('.')[0].split('_')[1])
        except IndexError:
            page_count = 1

        url = response.url[:-5]
        for i in range(2, page_count + 1):
            link = url + '_' + str(i) + '.aspx'
            self.crawl(link, callback=self.next_list)

        t = soup('ul', {'class':'News_list'})[0].find_all('li')
        domain = 'http://www.stghj.gov.cn'
        for i in t:
            link = domain + i.find_all('a')[0]['href']
            print(link)
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('ul', {'class':'News_list'})[0].find_all('li')
        domain = 'http://www.stghj.gov.cn'
        for i in t:
            link = domain + i.find_all('a')[0]['href']
            print(link)
            self.crawl(link, callback=self.content_page) 