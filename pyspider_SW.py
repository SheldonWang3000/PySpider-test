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
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[7], 'source':'GH'})
        self.crawl('http://www.swghj.gov.cn/gs/gsgd.html', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[6], 'source':'GH'})

        self.crawl('http://www.swgtj.gov.cn/Smallclass_537.html?page=1',
            callback=self.land_page, age=1,
            save={'type':self.table_name[14], 'source':'GT'})

    def land_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        page_count = int(soup('a', {'id':'endPage'})[0]['href'].split('?')[1].split('=')[1])
        url, params = self.get_params(response)
        for i in range(2, page_count + 1):
            params['page'] = str(i)
            self.crawl(url, params=params, age=1, save=response.save, callback=self.land_list_page)

        lists = soup('td', {'bgcolor':'#FFFFFF'})[-1].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lists = soup('td', {'bgcolor':'#FFFFFF'})[-1].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)

        next_link = ''
        t = soup('a')
        for i in t:
            if i.get_text() == '上一页':
                link = urljoin(response.url, i['href'])
                next_link = link
                self.crawl(link, callback=self.plan_page, age=1, save=response.save) 
                break

        lists = soup.find('table', {'width':'100%'}).find_all('a', href=True)
        print(len(lists))
        for i in lists:
            if i.get_text() != '下一页':
                link = urljoin(response.url, i['href'])
                if link != next_link:
                    print(link)
                    self.crawl(link, callback=self.content_page, save=response.save)

        