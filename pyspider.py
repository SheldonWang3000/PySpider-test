from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq
import re
import urllib2
import os
from cStringIO import StringIO
from PIL import Image
import urlparse
from multiprocessing.dummy import Pool as ThreadPool 


class Handler(BaseHandler):
    num = 0
    height = 0
    width = 0
    thread_num = 8
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.laho.gov.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/index.htm', 
            fetch_type='js', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60)
    @config(age = 1)
    def index_page(self, response):
        for each in response.doc('a.cn').items():
            if pq(each).text() == u'下一页':
                self.crawl(each.attr.href, fetch_type='js', callback=self.index_page)
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://www\.laho\.gov\.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/\d+/t\d+_\d+\.htm\?num\=1', each.attr.href, re.U):
                self.crawl(each.attr.href, fetch_type='js', callback=self.content_page)
            # if re.match('http://www\.laho\.gov\.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/index_\d+\.htm', each.attr.href, re.U):
                

    @config(priority=2)
    def content_page(self, response):
        return {
            "type": 'content',
            "url": response.url,
            "attachment": response.doc('a[href$="doc"]') + response.doc('a[href$="pdf"]') + response.doc('a[href$=".jpg"]'),
            "images": response.doc('img'),
            "html": response.text,
        }
    
    def on_result(self, result):
        if result is not None: 
            path = 'D:/page/' + str(self.num) + '.txt'
            # path = '/root/page/' + str(self.num) + '.txt'

            attachment = result['attachment'] 
            attachment_list = []
            for each in attachment.items():
                attachment_list.append(each.attr.href)
            pool = ThreadPool(self.thread_num)
            pool.map(self.download_attachment, attachment_list)
            pool.close()

            image_list = []
            for each in result['images'].items():
                image_url = urlparse.urljoin(result['url'], each.attr.src)
                image_list.append(image_url)
            pool = ThreadPool(self.thread_num)
            pool.map(self.download_image, image_list)

            self.num += 1
            f = open(path, 'wb')
            f.write(result['url'].encode('utf-8'))
            f.close()
        super(Handler, self).on_result(result)

    def download_attachment(self, url):
        f = urllib2.urlopen(url)
        filepath = 'D:/attachment/' + os.path.basename(url)
        # filepath = '/root/attachment/' + os.path.basename(url)
        with open(filepath, 'wb') as code:
            code.write(f.read())

    def download_image(self, url):
        f = urllib2.urlopen(url)
        
        if self.height * self.width == 0:
            filepath = 'D:/image/' + os.path.basename(url)
            # filepath = '/root/image/' + os.path.basename(url)
            with open(filepath, 'wb') as code:
                code.write(f.read())
        else:
            i = Image.open(StringIO(f.read()))
            temp_width, temp_height = i.size
            if temp_width >= self.width and temp_height >= self.height:
                filepath = 'D:/image/' + os.path.basename(url)
                # filepath = '/root/image/' + os.path.basename(url)
                i.save(filepath)
