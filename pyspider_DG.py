#!/usr/bin/env python
from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from itertools import repeat
import md5
import re
import urllib
import urllib2
import os
from cStringIO import StringIO
'''on CentOS'''
# from PIL import Image
'''on Ubuntu'''
import Image
import urlparse
from multiprocessing.dummy import Pool as ThreadPool 
import threading
import redis
'''东莞'''

class Handler(BaseHandler):
    r = redis.Redis()
    key = 'download'
    height = 250
    width = 250
    thread_num = 14
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
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9&1', 
        #     fetch_type='js', callback=self.index_page, save=1)
        # self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%D3%C3%B5%D8%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&1', 
        #     fetch_type='js', callback=self.index_page, save=1)
        # self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%B9%A4%B3%CC%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&1', 
            fetch_type='js', callback=self.index_page, save=1)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
      
        last_page = int(soup.find(id=re.compile(r'LabelPageCount')).get_text())
        if last_page != response.save:
            parmas = {'__EVENTTARGET': 'GridView1$ctl23$LinkButtonNextPage',
            '__EVENTARGUMENT': '', 
            }
            parmas['__VIEWSTATE'] = soup.find('input', {'name': '__VIEWSTATE'})['value']
            parmas['__EVENTVALIDATION'] = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
            parmas['GridView1$ctl23$tbPage'] = str(response.save)

            data = urllib.urlencode(parmas)
            url = 'http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9'
            url = url + '&' + str(response.save + 1)
            self.crawl(url, method='POST', data=data, callback=self.index_page, save=int(response.save) + 1)

        content = response.doc('a[href^=http]')
        for i in content.items():
            link = i.attr.href
            link = link.encode('GB18030')
            # print link
            self.crawl(link, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        r = BeautifulSoup(response.text)
        json = r.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json)
        json_list = response_json['list']
        domain = 'http://www.upo.gov.cn'
        content_list = [domain + i['Url'] for i in json_list]

        for each in content_list:
            self.crawl(each, callback=self.content_page)

    @config(priority=2)
    def content_page(self, response):
        attachment = response.doc('a[href$="doc"]') + response.doc('a[href$="pdf"]') + response.doc('a[href$="jpg"]') + response.doc('a[href$="png"]') + response.doc('a[href$="gif"]')
        images = response.doc('img')

        url = response.url
        # f = open('/home/teer/urls.txt', 'a')
        # f.write(url)
        # f.write('\n')
        # f.close()
        # print url
        m = md5.new()
        m.update(url)
        web_name = m.hexdigest()
        # path = 'D:/web/' + web_name + '/'
        path = '/home/teer/web/' + web_name + '/'
        if not os.path.exists(path):
            os.makedirs(path)           

        attachment_list = []
        if attachment is not None:
            for each in attachment.items():
                attachment_list.append(each.attr.href)
            for i in attachment_list:
                d = {}
                d['url'] = i
                d['path'] = path
                d['type'] = 'attachment'
                self.r.rpush(self.key, str(d))
                # self.crawl(i, callback=self.attachment_page, save=path)
                # self.download_attachment(i, path)
                # t = threading.Thread(target=self.download_attachment, args=(i, path))
                # t.setDaemon(False)
                # t.start()
            # for link in attachment_list:
            # for link in attachment_list:
            #     self.crawl(link, callback=self.attachment_page, save=path)
            # pool = ThreadPool(len(attachment_list) if len(attachment_list) < self.thread_num else self.thread_num)
            # pool.map_async(self.download_attachment, zip(attachment_list, repeat(path)))
            # pool.close()

        image_list = []
        if images is not None:
            for each in images.items():
                image_url = urlparse.urljoin(url, each.attr.src)
                image_list.append(image_url)
            for i in image_list:
                d = {}
                d['url'] = i
                d['path'] = path
                d['type'] = 'image'
                self.r.rpush(self.key, str(d))
                # self.crawl(i, callback=self.image_page, save=path)
                # self.download_image(i, path)
                # t = threading.Thread(target=self.download_image, args=(i, path))
                # t.setDaemon(False)
                # t.start() 
            # for link in image_list:
            #     self.crawl(link, callback=self.image_page, save=path)
            # pool = ThreadPool(len(attachment_list) if len(attachment_list) < self.thread_num else self.thread_num)
            # pool.map_async(self.download_image, zip(image_list, repeat(path)))
            # pool.close()

        return {
            "url": response.url,
            "html": response.text,
        }

    def attachment_page(self, response):
        path = response.save
        url = response.url
        try:
            attachment_path = path + os.path.basename(url)
            f = urllib2.urlopen(url)
            with open(attachment_path, 'wb') as code:
                code.write(f.read())
        except urllib2.HTTPError:
            print '404'

    def image_page(self, response):
        url = response.url
        path = response.save
        try:
            if self.height * self.width == 0:
                image_path = path + os.path.basename(url)
                with open(image_path, 'wb') as code:
                    code.write(response.content)
            else:
                i = Image.open(StringIO(response.content))
                temp_width, temp_height = i.size
                if temp_width >= self.width and temp_height >= self.height:
                    image_path = path + os.path.basename(url)
                    try:
                        i.save(image_path)
                    except KeyError:
                        m = md5.new()
                        m.update(os.path.basename(url))
                        i.save(path + m.hexdigest() + '.' + i.format)
        except urllib2.HTTPError:
            print '404'

    def on_result(self, result):
        if result is not None: 
            m = md5.new()
            m.update(result['url'])
            web_name = m.hexdigest()
            # path = 'D:/web/' + web_name + '/'
            path = '/home/teer/web/' + web_name + '/'
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

    # def download_attachment(self, (url, path)):
    def download_attachment(self, url, path):
        try:
            attachment_path = path + os.path.basename(url)
            f = urllib2.urlopen(url)
            with open(attachment_path, 'wb') as code:
                code.write(f.read())
        except urllib2.HTTPError:
            print '404'

    # def download_image(self, (url, path)):
    def download_image(self, url, path):
        try:
            f = urllib2.urlopen(url)
            
            if self.height * self.width == 0:
                image_path = path + os.path.basename(url)
                with open(image_path, 'wb') as code:
                    code.write(f.read())
            else:
                i = Image.open(StringIO(f.read()))
                temp_width, temp_height = i.size
                if temp_width >= self.width and temp_height >= self.height:
                    image_path = path + os.path.basename(url)
                    try:
                        i.save(image_path)
                    except KeyError:
                        m = md5.new()
                        m.update(os.path.basename(url))
                        i.save(path + m.hexdigest() + '.' + i.format)
        except urllib2.HTTPError:
            print '404'
