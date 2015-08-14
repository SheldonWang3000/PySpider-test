from pyspider.libs.base_handler import *
from my import My
import os
from bs4 import BeautifulSoup
'''广州'''

class Handler(My):
    name = "GZ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=004&area=all&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=005&area=all&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=006&area=all&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[4], 'source':'GH'})
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=007&area=all&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.upo.gov.cn/WebApi/GsApi.aspx?do=phlist&lb=null&area=null&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[7], 'source':'GH'})
        self.crawl('http://www.upo.gov.cn/WebApi/GsApi.aspx?do=pclist&lb=null&area=null&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[6], 'source':'GH'})

        self.crawl('http://www.laho.gov.cn/ywpd/tdgl/zwxx/tdjyxx/cjgs/index.htm', age=1,
            fetch_type='js', callback=self.land_page, headers={},
            save={'type':self.table_name[14], 'source':'GT'},
            js_script='''function(){return nAllCount}''')

        self.crawl('http://gzcc2012.gzcc.gov.cn/zwgk/jgys.aspx',
            save={'type':self.table_name[15], 'source':'JS', 'page':'1'}, age=1,
            fetch_type='js', callback=self.build_page)

    def build_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        page_count = int(soup('a', 'a1')[-1]['href'].split(',')[1].split('\'')[1])

        data = {}
        data['__VIEWSTATE'] = soup('input', {'name':'__VIEWSTATE'})[0]['value']
        data['__EVENTTARGET'] = 'ASNPager1'
        data['__EVENTVALIDATION'] = soup('input', {'name':'__EVENTVALIDATION'})[0]['value']

        data['__EVENTARGUMENT'] = response.save['page']
        params = {}
        params['page'] = response.save['page']
        self.crawl(response.url, data=data, method='POST', age=1, params=params,
                save=response.save, fetch_type='js', callback=self.content_page)
        if response.save['page'] != str(page_count):
            response.save['page'] = str(int(response.save['page']) + 1)
            data['__EVENTARGUMENT'] = response.save['page']
            self.crawl(response.url, data=data, method='POST', age=1, 
                save=response.save, fetch_type='js', callback=self.build_page)   

    def land_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        page_count = int((int(response.js_script_result) + 14) / 15)
        # print(page_count)
        url = response.url
        url = url[:url.rfind('.')] + '_%s' + url[url.rfind('.'):]
        for i in range(1, page_count):
            link = url % str(i)
            self.crawl(link, callback=self.land_list_page, age=1, fetch_type='js',
                headers={}, save=response.save)

        lists = soup('dl', 'f_clear marginT10')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lists = soup('dl', 'f_clear marginT10')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)
        json = soup.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json)
        json_list = response_json['list']
        domain = 'http://www.upo.gov.cn'
        content_list = [self.real_path(domain, i['Url']) for i in json_list]
        page_count = response_json['pagecount']
        page_count = int(page_count)

        for each in content_list:
            self.crawl(each, callback=self.content_page, save=response.save)

        ajax_url = response.url[:-1]
        for i in range(2, page_count + 1):
            next_page = ajax_url + str(i)
            self.crawl(next_page, callback=self.plan_list_page, 
                age=1, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)
        # url = response.url
        # params_str = url.split('?')[1]
        # params = {}
        # for i in params_str.split('&'):
        #     temp = i.split('=')
        #     params[temp[0]] = temp[1]
        # page = int(params['page'])
        # print(page)
        json = soup.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json)
        json_list = response_json['list']
        domain = 'http://www.upo.gov.cn'
        content_list = [self.real_path(domain, i['Url']) for i in json_list]

        for each in content_list:
            self.crawl(each, callback=self.content_page, save=response.save)