from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
from my import My
import re

'''潮州'''

class Handler(My):
    name = 'CZ'

    @every(minutes = 24 * 60)
    def on_start(self):
        self.crawl('http://czcsgh.gov.cn/yishu_s.asp?Page=1', fetch_type='js',
            callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://czcsgh.gov.cn/jsyd_s.asp?Page=1', fetch_type='js', 
            callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://czcsgh.gov.cn/gcyd_s.asp?Page=1', fetch_type='js',
            callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://czcsgh.gov.cn/jsgcFj_s.asp?Page=1', fetch_type='js', 
            callback=self.index_page, save={'type':self.table_name[4]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)

        params_str = soup('a', {'href': re.compile(r'\?Page=\d+')})[-1]['href'].split('?')[-1].split('&')
        params = {}
        for i in params_str:
            if len(i) != 0:
                temp = i.split('=')
                params[temp[0]] = temp[1]

        print(params) 
        page_count = int(params['Page'])

        domain = response.url.split('?')[0]
        for i in range(2, page_count + 1):
            params['Page'] = str(i)
            self.crawl(domain, fetch_type='js', callback=self.content_page, 
                params=params, save=response.save)

        self.crawl(response.url, fetch_type='js', callback=self.content_page, 
            save=response.save, force_update=True)
