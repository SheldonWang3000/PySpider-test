from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''深圳'''

class Handler(My):
    name = "SZ"
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=xzyjsQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=jsydXkzQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=jsgcXkzQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=jsgcYshgzQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.plan_page, 
            age=1, save={'type':self.table_name[4], 'source':'GH'})

        self.crawl('http://www.szpl.gov.cn:8080/was5/web/search?page=1&channelid=235315&perpage=25&outlinepage=10',
            callback=self.land_page, save={'type':self.table_name[14], 'source':'GT'}, 
            age=1)
        self.crawl('http://www.szpl.gov.cn:8080/was5/web/search?page=1&channelid=290259&perpage=25&outlinepage=10',
            callback=self.land_page, save={'type':self.table_name[14], 'source':'GT'}, 
            age=1)

        self.crawl('http://61.144.226.2:8001/web/project/jgysAction.do?page=1&method=toList&method=toList&method=toList&method=toList&method=toList&method=toList',
            age=1, save={'type':self.table_name[15], 'source':'JS'}, callback=self.build_page)

    def build_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        t = soup('a', {'id':'lx'})
        params = {}
        for i in t[0]['href'].split('?')[1].split('&'):
            temp = i.split('=')
            params[temp[0]] = temp[1]
        page_count = int(params['page'])

        url, params = self.get_params(response)
        for i in range(2, page_count + 1):
            params['page'] = str(i)
            self.crawl(url, params=params, save=response.save,
                callback=self.build_list_page, age=1)

        domain = 'http://61.144.226.2:8001/web/project/jgysAction.do?method=toView&ndxh=%s'
        lists = soup('table', {'id':'bean'})[0].find_all('a')
        for i in lists:
            link = domain % i.get_text()
            self.crawl(link, save=response.save, callback=self.content_page)

    def build_list_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        domain = 'http://61.144.226.2:8001/web/project/jgysAction.do?method=toView&ndxh=%s'
        lists = soup('table', {'id':'bean'})[0].find_all('a')
        for i in lists:
            link = domain % i.get_text()
            self.crawl(link, save=response.save, callback=self.content_page)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup('table', {'class':'tdown'})[0].find_all('td')[0].find_all('a')[-1]['href'].split('?')[-1].split('&')
        params = {}
        for i in table:
            if len(i) != 0:
                temp = i.split('=')
                params[temp[0]] = temp[1]
        page_count = int(params['pageNo'])
        domain = response.url.split('?')[0]
        for i in range(2, page_count + 1):
            params['pageNo'] = str(i)
            self.crawl(domain, fetch_type='js', params=params, 
                callback=self.content_page, save=response.save)

        self.crawl(response.url, fetch_type='js', 
            callback=self.content_page, age=1)

    def land_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        
        t = soup('a', 'last-page')[0]['href']
        params = {}
        for i in t.split('?')[1].split('&'):
            temp = i.split('=')
            params[temp[0]] = temp[1]
        page_count = int(params['page'])

        for i in range(2, page_count + 1):
            params['page'] = str(i)
            self.crawl(response.url.split('?')[0], age=1, params=params, callback=self.content_page,
                save=response.save)