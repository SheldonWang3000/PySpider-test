from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''深圳'''

class Handler(My):
    name = "SZ"
    mkdir = '/opt/web/'
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=xzyjsQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=jsydXkzQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=jsgcXkzQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://61.144.226.82/ghweb/main/zwgk/yssz/ysszResultViewAction.do?method=jsgcYshgzQuery&&order=0&sort=desc&pageNo=1', 
            fetch_type='js', callback=self.index_page, save={'type':self.table_name[4]})
    def index_page(self, response):
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
            callback=self.content_page, force_update=True)