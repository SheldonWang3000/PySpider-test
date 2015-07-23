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
'''珠海'''

class Handler(My):
    name = "ZH"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%d2%b5%ce%f1%b9%ab%ca%be&MdlName=%bd%a8%d6%fe%b9%a4%b3%cc%b9%e6%bb%ae%b9%ab%ca%be&page=1', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', {'class':'listFoot'})[0].find_all('a')[-1]['href'].split('&')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list)

        lists = soup('table')[2].find_all('a')
        domain = 'http://www.zhzgj.gov.cn/'
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table')[2].find_all('a')
        domain = 'http://www.zhzgj.gov.cn/'
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page) 