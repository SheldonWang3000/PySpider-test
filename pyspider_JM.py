from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
'''江门'''

class Handler(My):
    name = "JM"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=1&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=2&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=3&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=4&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[4]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('a', {'href': re.compile(r'spcs.asp')})[-1]['href'].split('?')[-1].split('&')
        params = {}
        for i in t:
            temp = i.split('=')
            params[temp[0]] = temp[1]
        page_count = int(params['page'])
        domain = 'http://ghj.jiangmen.gov.cn/spcs.asp'
        for i in range(1, page_count + 1):
            temp = params
            temp['page'] = str(i)
            self.crawl(domain, fetch_type='js',callback=self.content_page, 
                params=temp, save=response.save) 