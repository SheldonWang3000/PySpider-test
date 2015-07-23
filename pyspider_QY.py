from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import hashlib
import re
import os
import redis
from urllib.parse import urljoin 
from urllib.parse import urlparse
from urllib.parse import urlunparse
'''清远'''

class Handler(BaseHandler):
    name = "QY"
    mkdir = '/home/sheldon/web/'
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
        # self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_site_submission&page=1', callback=self.index_page)
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=businesses_project_planning_permit&page=1', callback=self.index_page)
        # self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_planning_permit&page=1', callback=self.index_page)
        # self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=village_project_planning_permit&page=1', callback=self.index_page)
        # self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_planning_acceptance&page=1', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        r = BeautifulSoup(response.text)
        page_count = int(r('table', {'class':'p-table'})[0].find_all('td')[0].get_text().split('\n')[1][5:])
        per_page = int(r('table', {'class':'p-table'})[0].find_all('td')[0].get_text().split('\n')[2][:-5])
        pages = int(page_count / per_page) if page_count % per_page == 0 else int(page_count / per_page) + 1
        print(pages)
        url = response.url[:-1]
        for i in range(2, pages + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list)

        domain = 'http://120.81.224.155:8084/project/show.php?id=%s&typeform=%s'
        lists = r('ul', {'class':'list'})[0].find_all('li')[1:]
        for i in lists:
            key = i.a['onclick']
            key = key[8:len(key) - 1]
            keys = key.split(',')
            request_id = keys[0]
            request_method = keys[1]
            request_method = request_method[1:len(request_method) - 1]
            link = domain % (request_id, request_method)
            # print link
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        r = BeautifulSoup(response.text)
        domain = 'http://120.81.224.155:8084/project/show.php?id=%s&typeform=%s'
        lists = r('ul', {'class':'list'})[0].find_all('li')[1:]
        for i in lists:
            key = i.a['onclick']
            key = key[8:len(key) - 1]
            keys = key.split(',')
            request_id = keys[0]
            request_method = keys[1]
            request_method = request_method[1:len(request_method) - 1]
            link = domain % (request_id, request_method)
            self.crawl(link, callback=self.content_page)

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