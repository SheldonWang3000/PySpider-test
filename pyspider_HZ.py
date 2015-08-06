from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import time
import xmltodict
'''惠州'''

class Handler(My):
    name = "HZ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_xzyjs/index.html', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[0]})
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_ydghxkz/index.html', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[1]})
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_gcghxkz/index.html', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[2]})
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_ghyshgz/index.html', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[4]})
    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        t = soup('script', {'language':'JavaScript'})
        l = t[1].get_text().split('\'')
        x = l[13]
        d = xmltodict.parse(x)
        k = d['xml']['RECS']['INFO']
        links = []
        for i in k:
            links.append(i['InfoURL'])
        url = "http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/"
        for i in links:
            link = self.real_path(url, i)
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save)
            time.sleep(0.1)  