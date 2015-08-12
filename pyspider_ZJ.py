from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
from urllib.parse import urlencode

'''湛江'''

class Handler(My):
    name = "ZJ"
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zjgh.gov.cn/ysszgs.aspx?classid=21&1', 
            callback=self.plan_page, age=1, 
            save={'page':1, 'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://www.zjgh.gov.cn/ysszgs.aspx?classid=22&1', 
            callback=self.plan_page, age=1, 
            save={'page':1, 'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.zjgh.gov.cn/ysszgs.aspx?classid=23&1', 
            callback=self.plan_page, age=1, 
            save={'page':1, 'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.zjgh.gov.cn/ysszgs.aspx?classid=24&1', 
            callback=self.plan_page, age=1, 
            save={'page':1, 'type':self.table_name[3], 'source':'GH'})

        self.crawl('http://www.zjlr.gov.cn/newslist.action?id=48&bigid=15',
            callback=self.land_page, age=1,
            save={'type':self.table_name[14], 'source':'GT'})
        self.crawl('http://www.zjlr.gov.cn/newslist.action?id=46&bigid=14',
            callback=self.land_page, age=1,
            save={'type':self.table_name[14], 'source':'GT'})

    def land_page(self, response):
        soup = BeautifulSoup(response.text)

        page_count = int(soup('div', {'class':'pg'})[0].find_all('a')[-2]['onclick'].split('(')[1].split(')')[0])
        url = self.get_params(response)[0]

        data = {}
        data['id'] = soup('input', {'name':'id'})[0]['value']
        data['bigid'] = soup('input', {'name':'bigid'})[0]['value']
        m = hashlib.md5()
        m.update(url.encode())
        for i in range(2, page_count + 1):
            data['page'] = str(i)
            taskid = m.hexdigest() + str(i)
            self.crawl(url, data=data, method='POST', age=1,
                callback=self.land_list_page, save=response.save,
                taskid=taskid)

        lists = soup('div', 'index_list')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('div', 'index_list')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        lists = soup('a', {'target':'_blank'})[:-3]
        print(len(lists))
        domain = 'http://www.zjgh.gov.cn/'
        for i in lists:
            crawl_link = domain + i['href'] 
            self.crawl(crawl_link, callback=self.content_page, save=response.save)
        try: 
            last_page = int(soup('a', {'href': re.compile(r'javascript:__doPostBack')})[-1]['href'].split(',')[1].split('\'')[1])
        except IndexError:
            last_page = response.save['page']
        if last_page != response.save['page']:
            parmas = {'__EVENTTARGET': 'ywgslist$AspNetPager1'}
            parmas['__EVENTARGUMENT'] = str(response.save['page'] + 1)
            parmas['__VIEWSTATE'] = soup.find('input', {'name':'__VIEWSTATE'})['value']
            parmas['__EVENTVALIDATION'] = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
            parmas['search$SearchStr'] = '请输入关键字'.encode('gb2312')
            parmas['search$ColumnIDDDL'] = soup.find('select', {'name': 'search$ColumnIDDDL'}).find('option', {'selected':'selected'})['value']
            parmas['ywgslist$AspNetPager1_input'] = str(response.save['page'])

            data = urlencode(parmas)
            print(response.orig_url)
            temp = response.orig_url.split('&')
            url = temp[0]
            for i in temp[1:-1]:
                url += '&' + i
            print(url)
            url = url + '&' + str(response.save['page'] + 1)
            response.save['page'] = response.save['page'] + 1
            self.crawl(url, method='POST', data=data, age=1, 
                callback=self.plan_page, save=response.save)

        