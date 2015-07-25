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
'''韶关'''

class Handler(My):
    name = "SG"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.sggh.gov.cn/Article_Class_Item.asp?ClassID=148&ChildClassID=219&page=1', callback=self.index_page)

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('a', {'href':re.compile(r'Article_Class')})[-1]['href'].split('&')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list)

        lists = soup('ul')[2].find_all('li')
        domain = 'http://www.sggh.gov.cn/'
        for i in lists:
            link = domain + i.find('a')['href']
            self.crawl(link, fetch_type='js', callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('ul')[2].find_all('li')
        domain = 'http://www.sggh.gov.cn/'
        for i in lists:
            link = domain + i.find('a')['href']
            self.crawl(link, fetch_type='js', callback=self.content_page)

    def real_path(self, path):
        arr = urlparse(path)
        real_path = os.path.normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, real_path, arr.params, arr.query, arr.fragment))

    @config(priority=2)
    def content_page(self, response):
        attachment = response.doc('a[href*=".doc"]') + response.doc('a[href*=".pdf"]') + response.doc('a[href*=".jpg"]') + response.doc('a[href*=".png"]') + response.doc('a[href*=".gif"]')
        images = response.doc('img')
        
        url = response.url
        m = hashlib.md5()
        m.update(url.encode())
        web_name = '/' + m.hexdigest() + '/'
        path = self.mkdir + self.name + web_name
        if not os.path.exists(path):
            os.makedirs(path)           

        image_list = []
        if images is not None:
            for each in images.items():
                image_url = self.real_path(urljoin(url, each.attr.src))
                if image_url not in image_list:
                    image_list.append(image_url)
            for i in image_list:
                d = {}
                d['url'] = i
                d['type'] = 'image'
                d['path'] = path
                self.r.rpush(self.key, str(d))

        attachment_list = []
        if attachment is not None:
            for each in attachment.items():
                if each.attr.href not in attachment_list and each.attr.href not in image_list:
                    attachment_list.append(each.attr.href)
            for i in attachment_list:
                d = {}
                d['url'] = i
                d['type'] = 'attachment'
                d['path'] = path
                self.r.rpush(self.key, str(d))

        images = response.doc('iframe')
        if images is not None:
            for each in images.items():
                src = each.attr.src
                params = src.split('&')
                data = {}
                for i in params:
                    temp = i.split('=')
                    data[temp[0]] = temp[1]
                image_url = urljoin(url, data['uf'])
                if image_url not in image_list:
                    image_list.append(image_url)

            for i in image_list:
                d = {}
                d['url'] = i
                d['type'] = 'image'
                d['path'] = path
                self.r.rpush(self.key, str(d))

        return {
            "url": response.url,
            "html": response.text,
        } 