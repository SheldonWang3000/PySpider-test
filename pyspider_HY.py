from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
'''河源'''

class Handler(My):
    name = "HY"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=282&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=301&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=403&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})

        self.crawl('http://gtj.heyuan.gov.cn/ggxx/ggxx_tdjy.jsp?pageNO=1&maxPage=100', 
            callback=self.land_page, age=1, 
            save={'type':self.table_name[14], 'source':'GT'})

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)
        a_list = soup('a', {'href': re.compile(r'page=')})
        if len(a_list) == 0:
            self.crawl(response.url, callback=self.content_page, age=1, save=response.save)
        else:
            temp = a_list[-1]['href'].split('?')
            params = {}
            for i in temp[1].split('&'):
                if len(i) != 0:
                    temp = i.split('=')
                    params[temp[0]] = temp[1]
            page_count = int(params['page'])

            for i in range(2, page_count + 1):
                params['page'] = str(i)
                self.crawl(response.url.split('?')[0], params=params, age=1, 
                    callback=self.content_page, save=response.save)

            self.crawl(response.url, callback=self.content_page, age=1, save=response.save)

    def land_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('a', {'target':'_blank'})

        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save,)

        if len(lists) == 15:
            url, params_str = response.url.split('?')
            params = {}
            for i in params_str.split('&'):
                temp = i.split('=')
                params[temp[0]] = temp[1]
            params['pageNO'] = str(int(params['pageNO']) + 1)
            self.crawl(url, params=params, callback=self.land_page, age=1,
                save=response.save)
