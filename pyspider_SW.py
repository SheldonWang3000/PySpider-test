from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
from urllib.request import urljoin

'''汕尾'''

class Handler(My):
    name = 'SW'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.swghj.gov.cn/gs/gd.htm', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[7], 'source':'GH'})
        self.crawl('http://www.swghj.gov.cn/gs/gsgd.html', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[6], 'source':'GH'})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)

        next_link = ''
        t = soup('a')
        for i in t:
            if i.get_text() == '上一页':
                link = urljoin(response.url, i['href'])
                next_link = link
                self.crawl(link, callback=self.index_page, force_update=True, save=response.save) 
                break

        lists = soup.find('table', {'width':'100%'}).find_all('a', href=True)
        print(len(lists))
        for i in lists:
            if i.get_text() != '下一页':
                link = urljoin(response.url, i['href'])
                if link != next_link:
                    print(link)
                    self.crawl(link, callback=self.content_page, save=response.save)

        