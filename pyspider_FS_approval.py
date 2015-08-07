from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
from urllib.parse import urlencode
'''佛山批前批后'''

class Handler(My):
    name = "FS_approval"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.fsgtgh.gov.cn/ywzt/cxgh/pqgs/index.htm', save={'type':self.table_name[6]}, 
            force_update=True, fetch_type='js', callback=self.index_page) 
        self.crawl('http://www.fsgtgh.gov.cn/ywzt/cxgh/phgg/index.htm', save={'type':self.table_name[6]}, 
            force_update=True, fetch_type='js', callback=self.index_page) 

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('div', {'id':'sub_table'})[0].find_all('tbody')[0].find_all('tr')
        for i in t:
            link = i.find_all('td')[1].find_all('a')[0]['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

        t = soup('span', 'page2')[0].find_all('a')[-1]['href']
        page_count = int(t.split('_')[1].split('.')[0])
        print(page_count)

        url = response.url.split('.')
        domain = url[0]
        for i in url[1:-1]:
            domain += '.' + i
        domain += '_%s.' + url[-1]
        print(domain)
        for i in range(1, page_count + 1):
            link = domain % i
            self.crawl(link, callback=self.next_list, force_update=True, 
                save=response.save, fetch_type='js')


    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('div', {'id':'sub_table'})[0].find_all('tbody')[0].find_all('tr')
        for i in t:
            link = i.find_all('td')[1].find_all('a')[0]['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')