from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
'''江门'''

class Handler(My):
    name = "JM"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=1&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=2&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=3&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://ghj.jiangmen.gov.cn/spcs.asp?rstype=4&page=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[4], 'source':'GH'})

        self.crawl('http://gtj.jiangmen.gov.cn/jmgtj/RemiseList.aspx',
            save={'type':self.table_name[14], 'source':'GT', 'page':'1'}, 
            callback=self.land_page, age=1) 
        self.crawl('http://gtj.jiangmen.gov.cn/jmgtj/RemiseList.aspx?page=1',
            save={'type':self.table_name[14], 'source':'GT'}, 
            callback=self.content_page, age=1)
        

    def land_page(self, response):
        next_tag = response.doc('.NextBtnCSS')
        if next_tag.outerHtml() is not None:
            arguments = next_tag.attr.href[24:-1].replace('\'','').split(',')
            data = {}
            data['__EVENTTARGET'] = arguments[0]
            data['__EVENTARGUMENT'] = arguments[1] 
            data['__VIEWSTATE'] = str(response.doc('#__VIEWSTATE').attr.value)
            data['__VIEWSTATEGENERATOR'] = str(response.doc('#__VIEWSTATEGENERATOR').attr.value)
            data['__EVENTVALIDATION'] = str(response.doc('#__EVENTVALIDATION').attr.value)
            data['AxGridView1$ctl18$ctl04'] = 15
            data['AxGridView1$ctl18$ctl05'] = 1
            data['txtExamineNo'] = ''
            data['__VIEWSTATEENCRYPTED'] = ''
            params = {}
            params['page'] = str(int(response.save['page']) + 1)
            save_dict = response.save
            save_dict['page'] = str(int(save_dict['page']) + 1)
            self.crawl(response.url, method='POST', age=1, save=save_dict, 
                callback=self.land_page, data=data)
            self.crawl(response.url, params=params, 
                method='POST', age=1, save=save_dict, 
                callback=self.content_page, data=data)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('a', {'href': re.compile(r'spcs.asp')})[-1]['href'].split('?')[-1].split('&')
        params = {}
        for i in t:
            temp = i.split('=')
            params[temp[0]] = temp[1]
        page_count = int(params['page'])
        domain = 'http://ghj.jiangmen.gov.cn/spcs.asp'
        for i in range(1, page_count + 1):
            temp = params
            temp['page'] = str(i)
            self.crawl(domain, fetch_type='js', callback=self.content_page, 
                params=temp, save=response.save, age=1) 