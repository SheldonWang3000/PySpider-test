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
'''肇庆'''

class Handler(My):
    name = "ZQ"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zqplan.gov.cn/ghxk.aspx?flag=1', callback=self.index_page)
        self.crawl('http://www.zqplan.gov.cn/ghxk.aspx?flag=2', callback=self.index_page)
        self.crawl('http://www.zqplan.gov.cn/ghxk.aspx?flag=3', callback=self.index_page)
        # self.crawl('http://www.zqplan.gov.cn/ghxk.aspx?flag=5', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', {'class':'badoo'})[0].find_all('a')[-1]['href'].split('_')[1])

        flag = response.url[-1]
        url = 'http://www.zqplan.gov.cn/ghxk_%s_%s____0.aspx'
        for i in range(2, page_count + 1):
            link = url % (i, flag)
            self.crawl(link, callback=self.next_list)
        domain = 'http://www.zqplan.gov.cn/'
        lists = soup('table')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = domain + i['href']
            print(link)
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        domain = 'http://www.zqplan.gov.cn/'
        lists = soup('table')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = domain + i['href']
            print(link)
            self.crawl(link, callback=self.content_page) 