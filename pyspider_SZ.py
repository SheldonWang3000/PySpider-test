from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import quote
import redis
'''深圳'''

class Handler(My):
    name = "SZ"
    mkdir = '/home/sheldon/web/'
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.szpl.gov.cn/xxgk/tzgg/csghgg/index.html', 
            fetch_type='js', callback=self.index_page)

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
     
        lists = soup('a', {'target':'_blank'})[1:-2] 
        domain = response.url
        for i in lists:
            crawl_link = urljoin(domain, i['href'])
            self.crawl(crawl_link, fetch_type='js', callback=self.content_page)

        last_page = int(soup('a', {'target':'_self'})[-1]['href'].split('_')[1].split('.')[0])
        url = response.url 
        url = url.split('.')
        link = url[0]
        for i in url[1:-1]:
            link += '.' + i
        for i in range(1, last_page + 1):
            crawl_link = link + '_' + str(i) + '.' + url[-1]
            # print(crawl_link)
            self.crawl(crawl_link, fetch_type='js', callback=self.next_list)

    def next_list(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lists = soup('a', {'target':'_blank'})[1:-2] 
        domain = response.url
        for i in lists:
            crawl_link = urljoin(domain, i['href'])
            self.crawl(crawl_link, fetch_type='js', callback=self.content_page)