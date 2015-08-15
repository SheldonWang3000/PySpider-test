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
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=71&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=72&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[4], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=126&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.yjjs.gov.cn/list_nmag.asp?classid=127&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})

        self.crawl('http://www.yjlr.gov.cn/NewsList.asp?SortID=19&Page=1',
            callback=self.land_page, age=1,
            save={'type':self.table_name[14], 'source':'GT'})

        self.crawl('http://www.yjjs.gov.cn/list.asp?classid=73&page=1',
            callback=self.plan_page, age=1,
            save={'type':self.table_name[15], 'source':'JS'})

    def land_page(self, response):
        soup = BeautifulSoup(response.text)    
        page_count = int((int(soup('div', 'Bodyer_right_page_end')[0].find('font').get_text()) + 24) / 25)
        url, params = self.get_params(response)
        for i in range(2, page_count + 1):
            params['Page'] = str(i)
            self.crawl(url, params=params, save=response.save,
                callback=self.land_list_page, age=1)

        lists = soup.find_all('div', 'news_list')
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup.find_all('div', 'news_list')
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_page(self, response):
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
                    age=1, save=response.save)
            elif temp[3] == '1':
                crawl_link = domain + temp[0] 
                self.crawl(crawl_link, callback=self.content_page, 
                    age=1, save=response.save)

        last_page = int(soup('strong')[0].get_text().split('/')[1])
        url = response.url[:-1]
        for i in range(2, last_page + 1):
            crawl_link = url + str(i)
            # print(crawl_link)
            self.crawl(crawl_link, callback=self.plan_list_page, 
                age=1, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lists = soup('a', {'onclick': re.compile(r'titlelinks')})
        domain = 'http://www.yjjs.gov.cn/news_Info.asp?rs_id='
        for i in lists:
            crawl_link = domain + i['onclick'].split('(')[1].split(',')[0]
            self.crawl(crawl_link, callback=self.content_page, save=response.save)