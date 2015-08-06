from pyspider.libs.base_handler import *
from my import My
import os
from bs4 import BeautifulSoup
'''广州市国土资源和规划委员会'''

class Handler(My):
    name = "GZ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=004&area=all&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=005&area=all&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=006&area=all&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[4]})
        self.crawl('http://www.upo.gov.cn/WebApi/SzskgkApi.aspx?do=list&lb=007&area=all&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://www.upo.gov.cn/WebApi/GsApi.aspx?do=phlist&lb=null&area=null&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[7]})
        self.crawl('http://www.upo.gov.cn/WebApi/GsApi.aspx?do=pclist&lb=null&area=null&page=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[6]})

    def index_page(self, response):
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
            self.crawl(next_page, callback=self.next_list, save=response.save)

    @config(priority=2)
    def next_list(self, response):
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