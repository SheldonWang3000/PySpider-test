from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''茂名'''

class Handler(My):
    name = "MM"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=1&page=1', 
            callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=2&page=1', 
            callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=3&page=1', 
            callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=4&page=1', 
            callback=self.index_page, save={'type':self.table_name[4]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)

        t = soup('div', {'class':'pagebar'})[0].get_text()
        k = t.split(' ')[0] 
        page_count = int(k[1: len(k) - 3])

        pages = int(page_count / 21) if page_count % 21 == 0 else int(page_count / 21) + 1
        url = response.url[:-1]
        for i in range(2, pages+ 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list, save=response.save)

        domain = 'http://csgh.maoming.gov.cn/'
        links = soup('table', {'id':'bookindex'})[0].find_all('a')
        for i in links:
            link = domain + i['href']
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        domain = 'http://csgh.maoming.gov.cn/'
        links = soup('table', {'id':'bookindex'})[0].find_all('a')
        for i in links:
            link = domain + i['href']
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save)