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

        self.crawl('http://www.sz68.com/land/?s=0',
            callback=self.land_page, save={'type':self.table_name[14], 'source':'GT'}, 
            age=1)

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

        lists = soup('table', {'style': 'border-top: 0px #ccc solid ;border-bottom: 0px #ccc solid;margin: 0 0 0 0;'})
        lists = lists[0].find_all('div', {'style':'float:right;'})
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, callback=self.content_page, save=response.save)
        
        params = {}
        for i in response.url.split('?')[1].split('&'):
            temp = i.split('=')
            params[temp[0]] = int(temp[1])
        if params['s'] == 0:
            page_count = int(soup('div', {'id':'wp_page_numbers'})[0].find_all('li')[-3].find('a')['href'].split('=')[1])
            for i in range(1, page_count + 1):
                params = {}
                params['s'] = i
                link = response.url.split('?')[0]
                self.crawl(link, age=1, params=params, callback=self.land_page,
                    save=response.save)