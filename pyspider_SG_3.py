from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
from urllib.parse import quote
'''韶关'''

class Handler(My):
    name = "SG_3"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!deptgovp_list.action?deptId=547&titleTypeId=605&siteOrgCode=440200&pagesize=15&action=show&pager.offset=0&currentpage=1&pagesize=15', 
            callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!deptgovp_list.action?deptId=547&titleTypeId=606&siteOrgCode=440200&pagesize=15&action=show&pager.offset=0&currentpage=1&pagesize=15', 
            callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!deptgovp_list.action?deptId=547&titleTypeId=607&siteOrgCode=440200&pagesize=15&action=show&pager.offset=0&currentpage=1&pagesize=15', 
            callback=self.index_page, save={'type':self.table_name[2]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', 'list_page')[0].find('table').find_all('a')[-1]['onclick'].split(',')[1].strip('\''))

        url = response.url
        params_str = url.split('?')[1].split('&')
        params = {}
        for i in params_str:
            if len(i) != 0:
                temp = i.split('=') 
                params[temp[0]] = temp[1]

        for i in range(2, page_count + 1):
            link = url.split('?')[0]
            params['currentpage'] = str(i)
            self.crawl(link, callback=self.next_list, params=params, save=response.save)

        lists = soup('table', 'service_table')[0].find_all('a')
        domain = 'http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!single.action'
        for i in lists:
            params_list = i['onclick'].split('(')[1].split(')')[0].split(',')
            params_list = [j.strip('\'') for j in params_list]
            params = {}
            params['deptId'] = params_list[0] 
            params['filePath'] = params_list[1]
            self.crawl(domain, fetch_type='js', params=params, 
                callback=self.iframe_page, save=response.save)

    @config(priority=2)
    def iframe_page(self, response):
        soup = BeautifulSoup(response.text)
        iframe = soup('iframe')[1]
        link = self.real_path('http://zwgk.sg.gov.cn/', iframe['src'])
        self.crawl(link, fetch_type='js', save=response.save, callback=self.content_page)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table', 'service_table')[0].find_all('a')
        domain = 'http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!single.action'
        for i in lists:
            params_list = i['onclick'].split('(')[1].split(')')[0].split(',')
            params_list = [j.strip('\'') for j in params_list]
            params = {}
            params['deptId'] = params_list[0] 
            params['filePath'] = params_list[1]
            self.crawl(domain, fetch_type='js', params=params, 
                callback=self.iframe_page, save=response.save)