from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''梅州'''

class Handler(My):
    name = "MZ"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.meizhou.gov.cn/open/index.php?NodeID=872&u=19&page=1', 
            callback=self.plan_page, force_update=True, 
            save={'type':self.table_name[8], 'source':'GH'})

        self.crawl('http://www.mzgtzy.gov.cn/newsAction.do?method=queryNews&classId=020010350000001647&queryForward=xgxz&page=1', 
            callback=self.land_page, save={'type':self.table_name[14], 'source':'GT'},
            js_script='''function(){return document.all('orderBy').form.totalPages.value;}''', 
            fetch_type='js', force_update=True)
        self.crawl('http://www.mzgtzy.gov.cn/newsAction.do?method=queryNews&classId=020010350000001648&queryForward=xgxz&page=1', 
            callback=self.land_page, save={'type':self.table_name[14], 'source':'GT'},
            js_script='''function(){return document.all('orderBy').form.totalPages.value;}''', 
            fetch_type='js', force_update=True)

    def plan_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', {'class':'pages'})[0].find_all('a')[-1]['href'].split('&')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.plan_list_page, 
                force_update=True, save=response.save)

        lists = soup('ul', {'class':'dotlist'})[0].find_all('li')
        for i in lists:
            link = i.find('a')['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('ul', {'class':'dotlist'})[0].find_all('li')
        for i in lists:
            link = i.find('a')['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    def land_page(self, response):
        soup = BeautifulSoup(response.text)
        t = soup('table')[0].find_all('input')[:7]
        data = {}
        for i in t:
            data[i['name']] = i['value']

        page_count = int(response.js_script_result)
        url, params_str = response.url.split('?')
        params = {}
        for i in params_str.split('&'):
            temp = i.split('=') 
            params[temp[0]] = temp[1]

        for i in range(2, page_count + 1):
            data['gotoPage'] = str(i)
            params['page'] = str(i)
            self.crawl(url, params=params, method='POST', data=data,
                force_update=True, callback=self.land_list_page, fetch_type='js',
                save=response.save)

        lists = soup('a', {'class', 'fl'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('a', {'class', 'fl'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)
 

