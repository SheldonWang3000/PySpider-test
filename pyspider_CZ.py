from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
from my import My
import re

'''潮州'''

class Handler(My):
    name = 'CZ'

    @every(minutes = 24 * 60)
    def on_start(self):
        self.crawl('http://czcsgh.gov.cn/yishu_s.asp?Page=1', fetch_type='js',
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://czcsgh.gov.cn/jsyd_s.asp?Page=1', fetch_type='js', 
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://czcsgh.gov.cn/gcyd_s.asp?Page=1', fetch_type='js',
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://czcsgh.gov.cn/jsgcFj_s.asp?Page=1', fetch_type='js', 
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[4], 'source':'GH'})

        self.crawl('http://czcsgh.gov.cn/info.asp?Page=1&big=4&small=57', 
            save={'type':self.table_name[6], 'source':'GH'}, age=1, 
            fetch_type='js', callback=self.approval_page) 

        self.crawl('http://www.czsgtj.gov.cn/Index.aspx?MenuId=9&id=560683&ptd=4891317&pob=5&page=1',
            save={'type':self.table_name[14], 'source':'GT'}, age=1, 
            fetch_type='js', callback=self.land_page)

    def certificate_page(self, response):
        soup = BeautifulSoup(response.text)

        params_str = soup('a', {'href': re.compile(r'\?Page=\d+')})[-1]['href'].split('?')[-1].split('&')
        params = {}
        for i in params_str:
            if len(i) != 0:
                temp = i.split('=')
                params[temp[0]] = temp[1]

        print(params) 
        page_count = int(params['Page'])

        domain = response.url.split('?')[0]
        for i in range(2, page_count + 1):
            params['Page'] = str(i)
            self.crawl(domain, fetch_type='js', callback=self.content_page, 
                params=params, save=response.save, age=1)

        self.crawl(response.url, fetch_type='js', callback=self.content_page, 
            save=response.save, age=1)

    def approval_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('a', {'target':'_blank', 'href': re.compile(r'infolist')})
        for i in t:
            link = i['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

        t = soup('td', {'width':'60'})[0].find_all('a')
        if len(t) != 0:
            link = self.real_path(response.url, t[0]['href']) 
            self.crawl(link, callback=self.approval_page, save=response.save, 
                fetch_type='js', age=1)

    def land_page(self, response):
        soup = BeautifulSoup(response.text)

        page_count = int(soup('div', {'class':'NormalTextBox', 'style':'float:left;width:40%;NormalTextBox'})[1].find_all('font', {'color':'blue'})[-1].get_text())

        data = {}
        data['__EVENTTARGET'] = '_ctl4$_ctl0$Container1$_ctl1$_ctl0$Paging'
        data['__EVENTARGUMENT'] = ''
        data['__VIEWSTATE'] = soup('input', {'name':'__VIEWSTATE'})[0]['value']
        data['__VIEWSTATEGENERATOR'] = soup('input', {'name':'__VIEWSTATEGENERATOR'})[0]['value']
        data['__VIEWSTATEENCRYPTED'] = soup('input', {'name':'__VIEWSTATEENCRYPTED'})[0]['value']

        data['_ctl4:_ctl0:LeftPane1:_ctl1:_ctl0:Paging_input'] = soup('input', {'name':'_ctl4:_ctl0:LeftPane1:_ctl1:_ctl0:Paging_input'})[0]['value']
        data['_ctl4:_ctl0:Container1:_ctl1:_ctl0:Paging_input'] = soup('input', {'name':'_ctl4:_ctl0:Container1:_ctl1:_ctl0:Paging_input'})[0]['value']
        data['_ctl5:_ctl0:LeftPane1:_ctl1:_ctl0:Paging_input'] = soup('input', {'name':'_ctl5:_ctl0:LeftPane1:_ctl1:_ctl0:Paging_input'})[0]['value']
        data['_ctl6:_ctl0:Container1:_ctl1:_ctl0:Paging_input'] = soup('input', {'name':'_ctl6:_ctl0:Container1:_ctl1:_ctl0:Paging_input'})[0]['value']

        url, params = self.get_params(response)
        for i in range(2, page_count + 1):
            data['__EVENTARGUMENT'] = str(i)
            params['page'] = str(i)
            self.crawl(url, data=data, params=params, method='POST',
                callback=self.land_list_page, age=1,
                save=response.save, fetch_type='js')

        lists = soup('table', {'id':'_ctl4__ctl0_Container1__ctl1__ctl0_dgArticleList01'})[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table', {'id':'_ctl4__ctl0_Container1__ctl1__ctl0_dgArticleList01'})[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

