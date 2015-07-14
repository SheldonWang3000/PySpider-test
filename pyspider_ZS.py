from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import hashlib
import re
import os
import redis
from urllib.parse import urljoin
'''中山'''

class Handler(BaseHandler):
    r = redis.Redis()
    key = 'download'
    headers= {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
    }
    crawl_config = {
        "headers" : headers,
        "timeout" : 100
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zsghj.gov.cn/list/p-5.html', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        r = BeautifulSoup(response.text)
        page_count = int(r.find_all('span', 'pageinfo')[0].find_all('strong')[0].get_text())

        url = 'http://www.zsghj.gov.cn/list/p-5-46-%s.html'
        for i in range(2, page_count + 1):
            link = url % (i)
            self.crawl(link, callback=self.next_list)
        domain = 'http://www.zsghj.gov.cn'
        lists = r.find_all('div', 'artlist')[0].find_all('li')
        for i in lists:
            link = domain + i.a['href']
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        r = BeautifulSoup(response.text)
        domain = 'http://www.zsghj.gov.cn'
        lists = r.find_all('div', 'artlist')[0].find_all('li')
        for i in lists:
            link = domain + i.a['href']
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def content_page(self, response):
        attachment = response.doc('a[href*=".doc"]') + response.doc('a[href*=".pdf"]') + response.doc('a[href*=".jpg"]') + response.doc('a[href*=".png"]') + response.doc('a[href*=".gif"]')
        images = response.doc('img')
        
        url = response.url
        m = hashlib.md5()
        m.update(url.encode())
        web_name = m.hexdigest()
        # path = 'D:/web/' + web_name + '/'
        path = '/home/teer/web/ZS/' + web_name + '/'
        if not os.path.exists(path):
            os.makedirs(path)           

        attachment_list = []
        if attachment is not None:
            for each in attachment.items():
                attachment_list.append(each.attr.href)
            for i in attachment_list:
                d = {}
                d['url'] = i
                d['type'] = 'attachment'
                d['path'] = path
                self.r.rpush(self.key, str(d))

        image_list = []
        if images is not None:
            for each in images.items():
                image_url = urljoin(url, each.attr.src)
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

    def on_result(self, result):
        if result is not None: 
            m = hashlib.md5()
            m.update(result['url'].encode())
            web_name = m.hexdigest()
            # path = 'D:/web/' + web_name + '/'
            path = '/home/teer/web/ZS/' + web_name + '/'
            if not os.path.exists(path):
                os.makedirs(path)           

            page_path = path + 'page.txt'
            f = open(page_path, 'wb')
            f.write(result['html'].encode('utf-8'))
            f.close()
            content_path = path + 'content.txt'
            f = open(content_path, 'wb')
            soup = BeautifulSoup(result['html'])
            for i in soup('style') + soup('script'):
                i.extract()
            content = soup.decode('utf-8')
            content = re.sub(r'<[/!]?\w+[^>]*>', '', content)
            content = re.sub(r'\s+', '', content)
            f.write(content.encode('utf-8'))
            f.close()
            url_path = path + 'url.txt'
            f = open(url_path, 'wb')
            f.write(result['url'].encode('utf-8'))
            f.close()
        super(Handler, self).on_result(result)