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
            callback=self.certificate_page, force_update=True, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://czcsgh.gov.cn/jsyd_s.asp?Page=1', fetch_type='js', 
            callback=self.certificate_page, force_update=True, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://czcsgh.gov.cn/gcyd_s.asp?Page=1', fetch_type='js',
            callback=self.certificate_page, force_update=True, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://czcsgh.gov.cn/jsgcFj_s.asp?Page=1', fetch_type='js', 
            callback=self.certificate_page, force_update=True, 
            save={'type':self.table_name[4], 'source':'GH'})

        self.crawl('http://czcsgh.gov.cn/info.asp?Page=1&big=4&small=57', 
            save={'type':self.table_name[6], 'source':'GH'}, force_update=True, 
            fetch_type='js', callback=self.approval_page) 

    def certificate_page(self, response):
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
                params=params, save=response.save, force_update=True)

        self.crawl(response.url, fetch_type='js', callback=self.content_page, 
            save=response.save, force_update=True)

    def approval_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('a', {'target':'_blank', 'href': re.compile(r'infolist')})
        for i in t:
            link = i['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

        t = soup('td', {'width':'60'})[0].find_all('a')
        if len(t) != 0:
            link = self.real_path(response.url, t[0]['href']) 
            self.crawl(link, callback=self.approval_page, save=response.save, 
                fetch_type='js', force_update=True)
