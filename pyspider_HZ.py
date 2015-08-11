from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import time
import xmltodict
'''惠州'''

class Handler(My):
    name = "HZ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_xzyjs/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[0]})
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_ydghxkz/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[1]})
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_gcghxkz/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[2]})
        self.crawl('http://ghjs.huizhou.gov.cn/business/htmlfiles/ghjsj/ph_ghyshgz/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[4]})
        self.crawl('http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/ghjsj/pq_xzyjs/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[9]})
        self.crawl('http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/ghjsj/pq_ydghxkz/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[10]})
        self.crawl('http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/ghjsj/pq_gcghxkz/index.html', 
            callback=self.plan_page, force_update=True, save={'type':self.table_name[11]})

        self.headers = {}
        self.headers['Accept'] = 'text/plain, */*; q=0.01'
        self.headers['Accept-Encoding'] = 'gzip, deflate'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Content-Length'] = '37'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cookie'] = 'ASP.NET_SessionId=2nilcdld2ldvwxctoix1ykld'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        self.headers['Origin'] = 'http://www.hzgtjy.com'
        self.headers['RA-Sid'] = '6FA100BB-20150228-025839-140a2d-0496ae'
        self.headers['RA-Ver'] = '3.0.7'
        self.headers['Referer'] = 'http://www.hzgtjy.com/index/Index4/'
        self.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        data = {} 
        data['page'] = 1
        data['size'] = 10
        data['orderBy'] = 'OFFERDATE-desc'
        self.crawl('http://www.hzgtjy.com/Index/PublicResults?page=1', method='POST', force_update=True,
            save={'type':self.table_name[14]}, headers=self.headers, data=data, callback=self.land_page)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        t = soup('script', {'language':'JavaScript'})
        l = t[1].get_text().split('\'')
        x = l[13]
        d = xmltodict.parse(x)
        k = d['xml']['RECS']['INFO']
        links = []
        for i in k:
            links.append(i['InfoURL'])
        url = "http://ghjs.huizhou.gov.cn/publicfiles/business/htmlfiles/"
        for i in links:
            link = self.real_path(url, i)
            # print(link)
            self.crawl(link, callback=self.content_page, save=response.save)
            time.sleep(0.1)  

    def land_page(self, response):
        null = ''
        true = 'true'
        false = 'false'
        json = eval(response.text)
        lists = json['data']
        domain = 'http://www.hzgtjy.com/Index/LandInfo/'
        for i in lists:
            link = domain + str(i['LANDINFO_ID'])
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')

        page_count = int((json['total'] + 9) / 10)
        url, params_str = response.url.split('?')
        params = {}
        for i in params_str.split('&'):
            temp = i.split('=')
            params[temp[0]] = temp[1]

        self.headers = {}
        self.headers['Accept'] = 'text/plain, */*; q=0.01'
        self.headers['Accept-Encoding'] = 'gzip, deflate'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Content-Length'] = '37'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cookie'] = 'ASP.NET_SessionId=2nilcdld2ldvwxctoix1ykld'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        self.headers['Origin'] = 'http://www.hzgtjy.com'
        self.headers['RA-Sid'] = '6FA100BB-20150228-025839-140a2d-0496ae'
        self.headers['RA-Ver'] = '3.0.7'
        self.headers['Referer'] = 'http://www.hzgtjy.com/index/Index4/'
        self.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'

        for i in range(2, page_count + 1):
            data = {'size':'10', 'orderBy':'OFFERDATE-desc'}
            data['page'] = str(i)
            params['page'] = str(i)
            self.crawl(url, params=params, data=data, method='POST', callback=self.land_list_page,
                force_update=True, save=response.save, headers=self.headers)

    def land_list_page(self, response):
        null = ''
        true = 'true'
        false = 'false'
        json = eval(response.text)
        lists = json['data']
        domain = 'http://www.hzgtjy.com/Index/LandInfo/'
        for i in lists:
            link = domain + str(i['LANDINFO_ID'])
            self.crawl(link, callback=self.content_page, save=response.save, fetch_type='js')
