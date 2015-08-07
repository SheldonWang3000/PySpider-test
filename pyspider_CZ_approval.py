from pyspider.libs.base_handler import *
import re
from my import My
from bs4 import BeautifulSoup
from urllib.parse import urlencode
'''潮州批前'''

class Handler(My):
    name = "CZ_approval"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://czcsgh.gov.cn/info.asp?Page=1&big=4&small=57', 
            save={'type':self.table_name[6]}, force_update=True, 
            fetch_type='js', callback=self.index_page) 

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('a', {'target':'_blank', 'href': re.compile(r'infolist')})
        for i in t:
            link = i['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

        t = soup('td', {'width':'60'})[0].find_all('a')
        if len(t) != 0:
            link = self.real_path(response.url, t[0]['href']) 
            self.crawl(link, callback=self.index_page, save=response.save, 
                fetch_type='js', force_update=True)