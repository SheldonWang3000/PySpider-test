from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''汕头'''

class Handler(My):
    name = "ST"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.stghj.gov.cn/Category_218/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_217/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_221/Index_1.aspx',
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_295/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_292/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_276/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_279/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_207/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[6], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_265/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[6], 'source':'GH'})
        self.crawl('http://www.stghj.gov.cn/Category_263/Index_1.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[6], 'source':'GH'})

        self.crawl('http://www.sttdkyjy.gov.cn/GuaPaiInfoList.aspx',
            save={'type':self.table_name[14], 'source':'GT'}, age=1,
            callback=self.land_page)

    def land_page(self, response):
        soup = BeautifulSoup(response.text)

        lists = soup('div', {'id':'tab1_1_content'})[0].find_all('a', {'target':'_self'}) 
        lists += soup('div', {'id':'tab1_2_content'})[0].find_all('a', {'target':'_self'})
        lists += soup('div', {'id':'tab1_3_content'})[0].find_all('a', {'target':'_self'})
        # print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.land_list_page, age=1,
                save=response.save)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table', {'rules':'all'})[0].find_all('a', {'target':'_self'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)
        try:
            t = soup('div', {'class':'pagecss'})[0].find_all('a')[-1]['href']   
        except IndexError:
            return 

        page_count = int(t.split('.')[0].split('_')[1])

        url = response.url[:-6]
        for i in range(2, page_count + 1):
            link = url + str(i) + '.aspx'
            self.crawl(link, callback=self.plan_list_page, age=1, save=response.save)

        t = soup('ul', {'class':'News_list'})[0].find_all('li')
        domain = 'http://www.stghj.gov.cn'
        for i in t:
            link = domain + i.find_all('a')[0]['href']
            # print(link_type)
            print(link)
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('ul', {'class':'News_list'})[0].find_all('li')
        domain = 'http://www.stghj.gov.cn'
        for i in t:
            link = domain + i.find_all('a')[0]['href']
            print(link)
            self.crawl(link, callback=self.content_page, save=response.save) 