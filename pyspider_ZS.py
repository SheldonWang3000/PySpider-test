from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import random

'''中山'''

class Handler(My):
    name = 'ZS'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zsghj.gov.cn/list/p-5.html', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[8], 'source':'GH'})

        self.crawl('http://www.zsfdc.gov.cn/ArticleList.aspx?id=33&page=1',
            callback=self.land_page, age=1, 
            save={'type':self.table_name[14], 'source':'GT'})

        self.crawl('http://www.zsjs.gov.cn/web/workOnline/queryProjectBackupsList?page=1&start=0&limit=20',
            callback=self.build_page, age=1,
            save={'type':self.table_name[15], 'source':'JS'})

    def build_page(self, response):
        null = ''
        true = 'true'
        false = 'false'
        json = eval(response.text)
        domain = 'http://www.zsjs.gov.cn/web/ysbaViewPage?id=%s'
        lists = json['rows']
        for i in lists:
            link = domain % i['id']
            self.crawl(link, save=response.save, callback=self.content_page)

        page_count = int((int(json['total']) + 19) / 20)
        url, params = self.get_params(response)
        for i in range(2, page_count + 1):
            params['page'] = str(i)
            params['start'] = str((i - 1) * 20)
            self.crawl(url, params=params, age=1, save=response.save, callback=self.build_list_page)

    def build_list_page(self, response):
        null = ''
        true = 'true'
        false = 'false'
        json = eval(response.text)
        domain = 'http://www.zsjs.gov.cn/web/ysbaViewPage?id=%s'
        lists = json['rows']
        for i in lists:
            link = domain % i['id']
            self.crawl(link, save=response.save, callback=self.content_page)

    def land_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        lists = soup('table', 'gridview')[0].find_all('a', {'target':'_blank'}) 
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

        if len(lists) == 20:
            data = {}
            data['__VIEWSTATE'] = soup.find('input', {'name':'__VIEWSTATE'})['value']
            data['__EVENTVALIDATION'] = soup.find('input', {'name':'__EVENTVALIDATION'})['value']
            data['ctl00$ContentPlaceHolder1$ibtNext.x'] = str(random.randint(0, 99))
            data['ctl00$ContentPlaceHolder1$ibtNext.y'] = str(random.randint(0, 99))
            url, params = self.get_params(response)
            params['page'] = str(int(params['page']) + 1)
            self.crawl(url, params=params, data=data, method='POST',
                save=response.save, age=1, callback=self.land_page)

    def plan_page(self, response):
        r = BeautifulSoup(response.text)
        page_count = int(r.find_all('span', 'pageinfo')[0].find_all('strong')[0].get_text())

        url = 'http://www.zsghj.gov.cn/list/p-5-46-%s.html'
        for i in range(2, page_count + 1):
            link = url % (i)
            self.crawl(link, callback=self.plan_list_page, age=1, save=response.save)
        domain = 'http://www.zsghj.gov.cn'
        lists = r.find_all('div', 'artlist')[0].find_all('li')
        for i in lists:
            link = domain + i.a['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        r = BeautifulSoup(response.text)
        domain = 'http://www.zsghj.gov.cn'
        lists = r.find_all('div', 'artlist')[0].find_all('li')
        for i in lists:
            link = domain + i.a['href']
            self.crawl(link, callback=self.content_page, save=response.save) 