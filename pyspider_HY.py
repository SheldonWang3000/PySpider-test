from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
'''河源'''

class Handler(My):
    name = "HY"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=282&page=1', 
            callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=301&page=1', 
            callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=403&page=1', 
            callback=self.index_page, save={'type':self.table_name[1]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        a_list = soup('a', {'href': re.compile(r'page=')})
        if len(a_list) == 0:
            self.crawl(response.url, callback=self.content_page, force_update=True, save=response.save)
        else:
            temp = a_list[-1]['href'].split('?')
            params = {}
            for i in temp[1].split('&'):
                if len(i) != 0:
                    temp = i.split('=')
                    params[temp[0]] = temp[1]
            page_count = int(params['page'])

            for i in range(2, page_count + 1):
                params['page'] = str(i)
                self.crawl(domain, params=params, callback=self.content_page, save=response.save)

            self.crawl(response.url, callback=self.content_page, force_update=True, save=response.save)