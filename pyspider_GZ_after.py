from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
import redis
'''广州市国土资源和规划委员会'''

class Handler(My):
    name = "GZ_after"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.upo.gov.cn/WebApi/GsApi.aspx?do=phlist&lb=null&area=null&page=1', 
            fetch_type='js', callback=self.index_page)

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        json = soup.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json)
        json_list = response_json['list']
        domain = 'http://www.upo.gov.cn'
        content_list = [domain + i['Url'] for i in json_list]
        page_count = response_json['pagecount']
        page_count = int(page_count)

        for each in content_list:
            self.crawl(each, callback=self.content_page)

        ajax_url = response.url[:-1]
        # page_count = 100
        for i in range(2, page_count + 1):
            next_page = ajax_url + str(i)
            self.crawl(next_page, callback=self.next_list)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        json = soup.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json)
        json_list = response_json['list']
        domain = 'http://www.upo.gov.cn'
        content_list = [domain + i['Url'] for i in json_list]

        for each in content_list:
            self.crawl(each, callback=self.content_page) 