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
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[8], 'source':'GH'})
        self.crawl('http://www.jygh.gov.cn/class_type.asp?zf11id=69&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[8], 'source':'GH'})

        self.crawl('http://www.gd-jygt.gov.cn/zwgk/yw/tdly/index.html',
            callback=self.land_page, age=1,
            save={'type':self.table_name[14], 'source':'GT'})

    def plan_page(self, response):
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
            self.crawl(link, callback=self.plan_list_page, age=1, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)

        domain = 'http://www.jygh.gov.cn/'
        lists = soup('table', {'align':'center'})[0].find_all('a')
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    def land_page(self, response):
        soup = BeautifulSoup(response.text)

        page_count = int((int(soup('a', {'title':'Total record'})[0].get_text()) + 24) / 25)
        domain = 'http://www.gd-jygt.gov.cn/zwgk/yw/tdly/index_%s.html'
        for i in range(2, page_count + 1):
            link = domain % str(i)
            self.crawl(link, save=response.save, age=1,
                callback=self.land_list_page)

        lists = soup('table', 'box')[0].find_all('li')
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table', 'box')[0].find_all('li')
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, save=response.save, callback=self.content_page)