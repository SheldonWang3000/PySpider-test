from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''中山'''

class Handler(My):
    name = 'ZS'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zsghj.gov.cn/list/p-5.html', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[8], 'source':'GH'})

    def index_page(self, response):
        r = BeautifulSoup(response.text)
        page_count = int(r.find_all('span', 'pageinfo')[0].find_all('strong')[0].get_text())

        url = 'http://www.zsghj.gov.cn/list/p-5-46-%s.html'
        for i in range(2, page_count + 1):
            link = url % (i)
            self.crawl(link, callback=self.next_list, force_update=True, save=response.save)
        domain = 'http://www.zsghj.gov.cn'
        lists = r.find_all('div', 'artlist')[0].find_all('li')
        for i in lists:
            link = domain + i.a['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        r = BeautifulSoup(response.text)
        domain = 'http://www.zsghj.gov.cn'
        lists = r.find_all('div', 'artlist')[0].find_all('li')
        for i in lists:
            link = domain + i.a['href']
            self.crawl(link, callback=self.content_page, save=response.save) 