from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''江门_新会分局'''

class Handler(My):
    name = "JM_X"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.xhplan.com/ghgs.asp?Page=1', 
            callback=self.index_page, save={'type':'Unknow'}})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('td', {'class':'numindex'})[0].find_all('a')[-1]['href'].split('?')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list, save=response.save)

        lists = soup('div', {'class':'doclist'})[0].find_all('li')
        domain = 'http://www.xhplan.com/'
        for i in lists:
            link = domain + i.find('a')['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('div', {'class':'doclist'})[0].find_all('li')
        domain = 'http://www.xhplan.com/'
        for i in lists:
            link = domain + i.find('a')['href']
            self.crawl(link, callback=self.content_page, save=response.save) 