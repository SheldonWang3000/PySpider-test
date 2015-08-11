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
'''揭阳'''

class Handler(My):
    name = 'JY'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.jygh.gov.cn/class_type.asp?zf11id=54&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[8], 'source':'GH'})
        self.crawl('http://www.jygh.gov.cn/class_type.asp?zf11id=69&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[8], 'source':'GH'})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)

        domain = 'http://www.jygh.gov.cn/'
        lists = soup('table', {'align':'center'})[0].find_all('a')
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save)

        t = soup('a', {'href': re.compile(r'class_type\.asp\?zf11id=\d+&page=\d+')})[-1]['href'].split('?')[1].split('&')
        params = {}
        for i in t:
            k = i.split('=')
            params[k[0]] = k[1]
        page_count = int(params['page'])
        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list, force_update=True, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)

        domain = 'http://www.jygh.gov.cn/'
        lists = soup('table', {'align':'center'})[0].find_all('a')
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save)