from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import hashlib
import re
import os
import redis
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import quote
'''放到python环境目录的site-packages下'''
class My(BaseHandler):

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
    def on_start(self):
        print('on_start')
        print(type(self))
        pass

    # def index_page(self, response):
    #     pass

    # def next_list(self, response):
    #     pass

    def real_path(self, path):
        arr = urlparse(path)
        real_path = os.path.normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, real_path, arr.params, arr.query, arr.fragment))

    @config(priority=2)
    def content_page(self, response):
        attachment = response.doc('a[href*=".doc"]') + response.doc('a[href*=".pdf"]') + response.doc('a[href*=".jpg"]') + response.doc('a[href*=".png"]') + response.doc('a[href*=".gif"]') + response.doc('a[href*=".zip"]') + response.doc('a[href*=".rar"]') 
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
                    '''此处需要处理,asp结尾也可能是需要的链接'''
                    t = re.search('.asp', image_url)
                    if t is None:
                        image_list.append(image_url)
            for i in image_list:
                d = {}
                k = i.split('/')
                link = k[0]
                for i in k[1:]:
                    link += '/'+ quote(i)
                # print(link)
                d['url'] = link
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
                # print(i)
                d['type'] = 'attachment'
                d['path'] = path
                k = i.split('/')
                link = k[0]
                for i in k[1:]:
                    link += '/'+ quote(i)
                # print(link)
                d['url'] = link
                self.r.rpush(self.key, str(d))

        return {
            "url": response.url,
            "html": response.text,
        }


    def on_result(self, result):
        if result is not None: 
            m = hashlib.md5()
            m.update(result['url'].encode())
            web_name = '/' + m.hexdigest() + '/'
            path = self.mkdir + self.name + web_name
            if not os.path.exists(path):
                os.makedirs(path)           

            page_path = path + 'page.txt'
            f = open(page_path, 'wb')
            f.write(result['html'].encode('utf-8'))
            f.close()
            content_path = path + 'content.txt'
            f = open(content_path, 'wb')
            soup = BeautifulSoup(result['html'], 'html.parser')
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
        super(My, self).on_result(result)