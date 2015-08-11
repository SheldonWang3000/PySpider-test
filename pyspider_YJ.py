from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
'''阳江'''

class Handler(My):
    name = "YJ"
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=70&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=71&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=72&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[4], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=126&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=127&page=1', 
            callback=self.index_page, force_update=True, 
            save={'type':self.table_name[2], 'source':'GH'})

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
     
        lists = soup('a', {'onclick': re.compile(r'titlelinks')})
        domain = 'http://www.yjjs.gov.cn/news_Info.asp?rs_id='
        for i in lists:
            temp = i['onclick']
            left = temp.find('(')
            right = temp.rfind(')')
            temp = temp[left + 1:right]
            temp = temp.split(',')
            if temp[3] == '2':
                print(temp[1])
                link = temp[1].strip('\'')
                self.crawl(link, callback=self.content_page, 
                    force_update=True, save=response.save)
            elif temp[3] == '1':
                crawl_link = domain + temp[0] 
                self.crawl(crawl_link, callback=self.content_page, 
                    force_update=True, save=response.save)

        last_page = int(soup('strong')[0].get_text().split('/')[1])
        url = response.url[:-1]
        for i in range(2, last_page + 1):
            crawl_link = url + str(i)
            # print(crawl_link)
            self.crawl(crawl_link, callback=self.next_list, 
                force_update=True, save=response.save)

    def next_list(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lists = soup('a', {'onclick': re.compile(r'titlelinks')})
        domain = 'http://www.yjjs.gov.cn/news_Info.asp?rs_id='
        for i in lists:
            crawl_link = domain + i['onclick'].split('(')[1].split(',')[0]
            self.crawl(crawl_link, callback=self.content_page, save=response.save)