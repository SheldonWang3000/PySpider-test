#!/usr/bin/env python
from pyspider.libs.base_handler import *
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
        '''url编码问题'''
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9&1', 
            fetch_type='js', callback=self.index_page, save=1)
        # self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%D3%C3%B5%D8%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&1', 
        #     fetch_type='js', callback=self.index_page, save=1)
        # self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%B9%A4%B3%CC%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&1', 
        #     fetch_type='js', callback=self.index_page, save=1)

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
            # import chardet
            # print response.url
            # print response.url.encode('utf-8')
            # print chardet.detect(str(response.url))
            url = 'http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9'
            # url = response.url.encode('GB18030')
            # url = url[:-1]
            # print url
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
        attachment = response.doc('a[href*=".doc"]') + response.doc('a[href*=".pdf"]') + response.doc('a[href*=".jpg"]') + response.doc('a[href*=".png"]') + response.doc('a[href*=".gif"]')
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

        return {
            "url": response.url,
            "html": response.text,
        }

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