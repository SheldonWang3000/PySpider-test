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

        self.crawl('http://gcjs.jiangmen.gov.cn/InfoList.aspx?type=XMJS_JGYS&page=1',
            age=1, save={'type':self.table_name[15], 'source':'JS'}, fetch_type='js',
            callback=self.build_page)
    
    def build_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')    

        page_count = int(soup('font', {'color':'red'})[1].get_text())

        url, params = self.get_params(response)
        if int(params['page']) != page_count:
            data = {}
            data['__VIEWSTATE'] = soup('input', {'name':'__VIEWSTATE'})[0]['value']
            data['__VIEWSTATEGENERATOR'] = soup('input', {'name':'__VIEWSTATEGENERATOR'})[0]['value']
            data['__EVENTARGUMENT'] = ''
            data['__VIEWSTATEENCRYPTED'] = ''
            data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$AxGridView1$ctl28$ctl03'
            data['__EVENTVALIDATION'] = soup('input', {'name':'__EVENTVALIDATION'})[0]['value']
            data['ctl00$top1$host'] = soup('input', {'name':'ctl00$top1$host'})[0]['value']
            data['ctl00$top1$keyword'] = soup('input', {'name':'ctl00$top1$keyword'})[0]['value']
            data['ctl00$top1$ColumnType'] = 'ALL'
            data['tl00$ContentPlaceHolder1$AxGridView1$ctl28$ctl07'] = '25'
            data['tl00$ContentPlaceHolder1$AxGridView1$ctl28$ctl08'] = params['page']
            params['page'] = str(int(params['page']) + 1)
            self.crawl(url, params=params, data=data, save=response.save, age=1, callback=self.build_page)

        lists = soup('table', {'id':'ctl00_ContentPlaceHolder1_AxGridView1'})[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page)



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