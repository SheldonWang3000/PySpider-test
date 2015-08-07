from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''肇庆'''

class Handler(My):
    name = "ZQ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_1____0.aspx', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[0]})
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_2____0.aspx', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[1]})
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_3____0.aspx',
            callback=self.index_page, force_update=True, save={'type':self.table_name[2]})
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_5____0.aspx',
            callback=self.index_page, force_update=True, save={'type':self.table_name[4]})
        self.crawl('http://www.zqplan.gov.cn/gs_1_17.aspx',
            callback=self.index_page, force_update=True, save={'type':self.table_name[6]})
        self.crawl('http://www.zqplan.gov.cn/gs_1_24.aspx',
            callback=self.index_page, force_update=True, save={'type':self.table_name[7]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', {'class':'badoo'})[0].find_all('a')[-1]['href'].split('_')[1].split('.')[0])

        flag = int(response.url.split('_')[2].split('.')[0])
        # flag = response.url[-1]
        if flag in [1, 2, 3, 5]:
            url = 'http://www.zqplan.gov.cn/ghxk_%s_%s____0.aspx'
        elif flag in [17, 24]:
            url = 'http://www.zqplan.gov.cn/gs_%s_%s.aspx'
        for i in range(2, page_count + 1):
            link = url % (i, flag)
            self.crawl(link, callback=self.next_list, force_update=True, save=response.save)
        domain = 'http://www.zqplan.gov.cn/'
        lists = soup('table')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(domain, i['href'])
            print(link)
            self.crawl(link, callback=self.content_page, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        domain = 'http://www.zqplan.gov.cn/'
        table = soup('table')
        if len(table) != 0:
            lists = table[0].find_all('a', {'target':'_blank'})
            for i in lists:
                link = self.real_path(domain, i['href'])
                print(link)
                self.crawl(link, callback=self.content_page, save=response.save) 