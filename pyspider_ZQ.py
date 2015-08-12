from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''肇庆'''

class Handler(My):
    name = "ZQ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_1____0.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_2____0.aspx', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_3____0.aspx',
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.zqplan.gov.cn/ghxk_1_5____0.aspx',
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[4], 'source':'GH'})
        self.crawl('http://www.zqplan.gov.cn/gs_1_17.aspx',
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[6], 'source':'GH'})
        self.crawl('http://www.zqplan.gov.cn/gs_1_24.aspx',
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[7], 'source':'GH'})

        self.crawl('http://www.zqgtzy.gov.cn/newsAction.do?method=queryNews&classId=020010350000000912&page=1',
            callback=self.land_page, age=1, fetch_type='js',
            save={'type':self.table_name[14], 'source':'GT'})

    def land_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        page_count = int(soup('input', {'name':'totalPages'})[0]['value'])
        data = {}
        data['classId'] = soup('input', {'name':'classId'})[0]['value']
        data['textGeneralType'] = soup('input', {'name':'textGeneralType'})[0]['value']
        data['curPageNo'] = soup('input', {'name':'curPageNo'})[0]['value']
        data['totalCnts'] = soup('input', {'name':'totalCnts'})[0]['value']
        data['totalPages'] = soup('input', {'name':'totalPages'})[0]['value']
        data['cntPerPage'] = soup('input', {'name':'cntPerPage'})[0]['value']
        data['SplitFlag'] = '1'
        data['orderBy'] = soup('input', {'name':'orderBy'})[0]['value']
        data['descOrAsc'] = soup('input', {'name':'descOrAsc'})[0]['value']
        # print(data['curPageNo'])
       
        url, params = self.get_params(response) 
        for i in range(2, page_count + 1):
            data['gotoPage'] = str(i) 
            params['page'] = str(i)
            self.crawl(url, params=params, data=data, method='POST',
                save=response.save, callback=self.land_list_page, 
                age=1, fetch_type='js') 

        lists = soup('ul', 'cbm-ul')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lists = soup('ul', 'cbm-ul')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def plan_page(self, response):
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
            self.crawl(link, callback=self.plan_list_page, age=1, save=response.save)
        domain = 'http://www.zqplan.gov.cn/'
        lists = soup('table')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(domain, i['href'])
            print(link)
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)
        domain = 'http://www.zqplan.gov.cn/'
        table = soup('table')
        if len(table) != 0:
            lists = table[0].find_all('a', {'target':'_blank'})
            for i in lists:
                link = self.real_path(domain, i['href'])
                print(link)
                self.crawl(link, callback=self.content_page, save=response.save) 