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
            method='POST',data=data, callback=self.certificate_page, force_update=True, 
            save={'action':'xzyjs','type':self.table_name[0]})
        params = {'strWhere' : '%2C%2C%2C', 'action': 'ydgh', 'pageIndex': '1', 'pageSize': '15'}
        data = urlencode(params)
        self.crawl('http://www.fsgh.gov.cn/GTGHService/home/SearchData/ydgh?page=1', 
            method='POST',data=data, callback=self.certificate_page, force_update=True,  
            save={'action':'ydgh','type':self.table_name[1]})
        params = {'strWhere' : '%2C%2C%2C', 'action': 'gcgh', 'pageIndex': '1', 'pageSize': '15'}
        data = urlencode(params)
        self.crawl('http://www.fsgh.gov.cn/GTGHService/home/SearchData/gcgh?page=1', 
            method='POST',data=data, callback=self.certificate_page, force_update=True,  
            save={'action':'gcgh','type':self.table_name[2]})

        self.crawl('http://www.fsgtgh.gov.cn/ywzt/cxgh/pqgs/index.htm', save={'type':self.table_name[6]}, 
            force_update=True, fetch_type='js', callback=self.approval_page) 
        self.crawl('http://www.fsgtgh.gov.cn/ywzt/cxgh/phgg/index.htm', save={'type':self.table_name[6]}, 
            force_update=True, fetch_type='js', callback=self.approval_page) 

    def certificate_page(self, response):
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
            self.crawl(temp_url, method='POST', data=temp_data, 
                callback=self.certificate_list_page, save=response.save, force_update=True)

    def certificate_list_page(self, response):
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

    def approval_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('div', {'id':'sub_table'})[0].find_all('tbody')[0].find_all('tr')
        for i in t:
            link = i.find_all('td')[1].find_all('a')[0]['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

        t = soup('span', 'page2')[0].find_all('a')[-1]['href']
        page_count = int(t.split('_')[1].split('.')[0])
        print(page_count)

        url = response.url.split('.')
        domain = url[0]
        for i in url[1:-1]:
            domain += '.' + i
        domain += '_%s.' + url[-1]
        print(domain)
        for i in range(1, page_count + 1):
            link = domain % i
            self.crawl(link, callback=self.approval_list_page, force_update=True, 
                save=response.save, fetch_type='js')

    def approval_list_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('div', {'id':'sub_table'})[0].find_all('tbody')[0].find_all('tr')
        for i in t:
            link = i.find_all('td')[1].find_all('a')[0]['href']
            link = self.real_path(response.url, link)
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')