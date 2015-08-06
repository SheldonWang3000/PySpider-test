from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
from urllib.parse import urlencode
'''佛山'''

class Handler(My):
    name = "FS"

    domains = {'xzyjs':'http://www.fsgh.gov.cn/GTGHService/ViewCase/jsxmghxzyjs/',
            'ydgh':'http://www.fsgh.gov.cn/GTGHService/ViewCase/ydghxkz/',
            'gcgh':'http://www.fsgh.gov.cn/GTGHService/ViewCase/gcghxkz/'}

    @every(minutes=24 * 60)
    def on_start(self):
        params = {'strWhere' : '%2C%2C%2C', 'action': 'xzyjs', 'pageIndex': '1', 'pageSize': '15'}
        data = urlencode(params)
        self.crawl('http://www.fsgh.gov.cn/GTGHService/home/SearchData/xzyjs?page=1', 
            method='POST',data=data, callback=self.index_page, 
            save={'action':'xzyjs','type':self.table_name[0]})
        params = {'strWhere' : '%2C%2C%2C', 'action': 'ydgh', 'pageIndex': '1', 'pageSize': '15'}
        data = urlencode(params)
        self.crawl('http://www.fsgh.gov.cn/GTGHService/home/SearchData/ydgh?page=1', 
            method='POST',data=data, callback=self.index_page, 
            save={'action':'ydgh','type':self.table_name[1]})
        params = {'strWhere' : '%2C%2C%2C', 'action': 'gcgh', 'pageIndex': '1', 'pageSize': '15'}
        data = urlencode(params)
        self.crawl('http://www.fsgh.gov.cn/GTGHService/home/SearchData/gcgh?page=1', 
            method='POST',data=data, callback=self.index_page, 
            save={'action':'gcgh','type':self.table_name[2]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        json_text = soup.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json_text)
        json_list = eval(response_json['datas'])
        domain = self.domains[response.save['action']]
        for i in json_list:
            print(i['4'])
        content_list = [domain + i['4'] for i in json_list]

        page_count = response_json['pageCount']
        page_count = int(page_count)
        # print(page_count)

        for each in content_list:
            # print(each)
            self.crawl(each, callback=self.content_page, save=response.save)

        for i in range(2, page_count + 1):
            temp_url = response.url.split('?')[0] + '?page=' + str(i)
            params = {'strWhere' : '%2C%2C%2C', 'pageSize': '15'}
            params['action'] = response.save['action']
            params['pageIndex'] = str(i)
            temp_data = urlencode(params)
            self.crawl(temp_url, method='POST', data=temp_data, callback=self.next_list, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        json_text = soup.body.text
        null = ''
        true = 'true'
        false = 'false'
        response_json = eval(json_text)
        json_list = eval(response_json['datas'])
        domain = self.domains[response.save['action']]
        for i in json_list:
            print(i['4'])
        content_list = [domain + i['4'] for i in json_list]

        for each in content_list:
            self.crawl(each, callback=self.content_page, save=response.save) 