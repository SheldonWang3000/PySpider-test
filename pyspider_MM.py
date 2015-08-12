from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''茂名'''

class Handler(My):
    name = "MM"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=1&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=2&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=3&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://csgh.maoming.gov.cn/active/show.ashx?action=certList&pwd=&chk=1&key=&no=&sid=4&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[4], 'source':'GH'})

        self.crawl('http://gtzyj.maoming.gov.cn/newsAction.do?method=queryNews&classId=020010350000000960&page=1',
            callback=self.land_page, save={'type':self.table_name[14], 'source':'GT'},
            age=1, fetch_type='js')

    def land_page(self, response):
        soup = BeautifulSoup(response.text)

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
        print(data['curPageNo'])
       
        url, params = self.get_params(response) 
        for i in range(2, page_count + 1):
            data['gotoPage'] = str(i) 
            params['page'] = str(i)
            self.crawl(url, params=params, data=data, method='POST',
                save=response.save, callback=self.land_list_page, 
                age=1, fetch_type='js') 

        lists = soup('div', 'text')
        for i in lists:
            link = self.real_path(response.url, i.find_all('a')[0]['href'])
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        print(soup('input', {'name':'curPageNo'})[0]['value'])

        lists = soup('div', 'text')
        for i in lists:
            link = self.real_path(response.url, i.find_all('a')[0]['href'])
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)

        t = soup('div', {'class':'pagebar'})[0].get_text()
        k = t.split(' ')[0] 
        page_count = int(k[1: len(k) - 3])

        pages = int(page_count / 21) if page_count % 21 == 0 else int(page_count / 21) + 1
        url = response.url[:-1]
        for i in range(2, pages+ 1):
            link = url + str(i)
            self.crawl(link, callback=self.plan_list_page, 
                age=1, save=response.save)

        domain = 'http://csgh.maoming.gov.cn/'
        links = soup('table', {'id':'bookindex'})[0].find_all('a')
        for i in links:
            link = domain + i['href']
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)
        domain = 'http://csgh.maoming.gov.cn/'
        links = soup('table', {'id':'bookindex'})[0].find_all('a')
        for i in links:
            link = domain + i['href']
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save)