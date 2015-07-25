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

    def js_css_download(self, response):
        # 存储位置
        path = response.save['path']
        file_name = response.save['name']
        # 创建目录
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + file_name, 'w') as f:
            f.write(response.text)

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

        soup = BeautifulSoup(response.text)

        script_tag = soup.find_all('script', src=True)
        for each in script_tag:
            js_m = hashlib.md5()
            js_m.update(each['src'].encode())
            js_name = js_m.hexdigest()
            # 获取访问地址
            request_url = self.real_path(urljoin(response.url, each['src']))
            # 改动网页 css 地址为相对地址
            each['src'] = js_name + '.js'
            # 爬取css文件
            self.crawl(request_url, fetch_type='js', callback = self.js_css_download, save = {'path':path, 'name':each['src']})

        css_tag = soup.find_all('link', type='text/css')
        for each in css_tag:
            css_m = hashlib.md5()
            css_m.update(each['href'].encode())
            css_name = css_m.hexdigest()
            # 获取访问地址
            request_url = self.real_path(urljoin(response.url, each['href']))
            # 改动网页 css 地址为相对地址
            each['href'] = css_name + '.css'
            # 爬取css文件
            self.crawl(request_url, callback = self.js_css_download, save = {'path':path, 'name':each['href']})

        images = soup('img')
        image_list = []
        if images is not None:
            for each in images:
                image_url = self.real_path(urljoin(url, each['src']))
                k = image_url.split('/')
                link = k[0]
                for i in k[1:]:
                    link += '/'+ quote(i)
                image_url = link
                if image_url not in image_list:
                    # t = re.search('.asp', image_url)
                    # if t is None:
                    image_list.append(image_url)
                    d = {}
                    d['type'] = 'image'
                    d['path'] = path
                    d['url'] = image_url
                    m = hashlib.md5()
                    m.update(image_url.encode())
                    if re.search('.jpg', image_url) is not None:
                        each['src'] = m.hexdigest() + '.jpg'
                    elif re.search('.png', image_url) is not None:
                        each['src'] = m.hexdigest() + '.png'
                    elif re.search('.gif', image_url) is not None:
                        each['src'] = m.hexdigest() + '.gif'
                    d['name'] = each['src']
                    self.r.rpush(self.key, str(d))

        attachments = soup('a', href=True)
        attachment_list = []
        if attachments is not None:
            for each in attachments:
                href = each['href']
                type_name = None
                if re.search('.jpg', href) is not None:
                    type_name = 'jpg'
                elif re.search('.png', href) is not None:
                    type_name = '.png'
                elif re.search('.gif', href) is not None:
                    type_name = '.gif'
                elif re.search('.doc', href) is not None:
                    type_name = '.doc'
                elif re.search('.pdf', href) is not None:
                    type_name = '.pdf'
                elif re.search('.zip', href) is not None:
                    type_name = '.zip'
                elif re.search('.rar', href) is not None:
                    type_name = '.rar'
                if type_name is not None:
                    attachment_url = self.real_path(urljoin(url, href))
                    k = attachment_url.split('/')
                    link = k[0]
                    for i in k[1:]:
                        link += '/'+ quote(i)
                    attachment_url = link
                    if attachment_url not in attachment_list and attachment_url not in image_list:
                       attachment_list.append(href)
                       d = {}
                       d['type'] = 'attachment'
                       d['path'] = path
                       d['url'] = attachment_url
                       m = hashlib.md5()
                       m.update(attachment_url.encode())
                       each['href'] = m.hexdigest() + '.' + type_name
                       d['name'] = each['href']
                       self.r.rpush(self.key, str(d))

        # 针对 background 属性
        for key in soup.find_all(background=True):
            image_url = self.real_path(urljoin(response.url, key['background']))
            k = image_url.split('/')
            link = k[0]
            for i in k[1:]:
                link += '/'+ quote(i)
            image_url = link
            if image_url not in image_list:
                image_list.append(image_url)
                d = {}
                d['type'] = 'image'
                d['path'] = path
                d['url'] = image_url
                m = hashlib.md5()
                m.update(image_url.encode())
                if re.search('.jpg', image_url) is not None:
                    each['src'] = m.hexdigest() + '.jpg'
                elif re.search('.png', image_url) is not None:
                    each['src'] = m.hexdigest() + '.png'
                elif re.search('.gif', image_url) is not None:
                    each['src'] = m.hexdigest() + '.gif'
                d['name'] = each['src']
                self.r.rpush(self.key, str(d))

        return {
            "url": response.url,
            "html": str(soup),
        }


    def on_result(self, result):
        if result is not None: 
            m = hashlib.md5()
            m.update(result['url'].encode())
            web_name = '/' + m.hexdigest() + '/'
            path = self.mkdir + self.name + web_name
            if not os.path.exists(path):
                os.makedirs(path)           

            page_path = path + 'page.html'
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