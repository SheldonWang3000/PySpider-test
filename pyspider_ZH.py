from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''珠海'''

class Handler(My):
    name = "ZH"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%D2%B5%CE%F1%B9%AB%CA%BE&MdlName=%D3%C3%B5%D8%C0%E0%B9%AB%CA%BE&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%d2%b5%ce%f1%b9%ab%ca%be&MdlName=%bd%a8%d6%fe%b9%a4%b3%cc%b9%e6%bb%ae%b9%ab%ca%be&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%D2%B5%CE%F1%B9%AB%CA%BE&MdlName=%BD%BB%CD%A8%D3%EB%CA%D0%D5%FE%B9%A4%B3%CC%B9%E6%BB%AE%C0%E0&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%d2%b5%ce%f1%b9%ab%ca%be&MdlName=%b9%e6%bb%ae%cc%f5%bc%fe%ba%cb%ca%b5&page=1', 
            callback=self.plan_page, age=1, 
            save={'type':self.table_name[4], 'source':'GH'})

        self.crawl('http://www.gtjzh.gov.cn/gtj/list.asp?id=56&Page=1',
            age=1, save={'type':self.table_name[14], 'source':'GT','flag':1},  
            callback=self.land_page, fetch_type='js')
        self.crawl('http://www.gtjzh.gov.cn/gtj/list.asp?id=57&Page=1',
            age=1, save={'type':self.table_name[14], 'source':'GT','flag':2},  
            callback=self.land_page, fetch_type='js')

        self.crawl('http://dmqzjj.doumen.gov.cn/zlaq/jgys/index.htm', 
            age=1, save={'type':self.table_name[15], 'source':'JS'},
            fetch_type='js', callback=self.build_page)

    def build_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        lists = soup('div', 'listr right')[0].find('ul').find_all('a', href=True)
        print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page, fetch_type='js')

        page_count = int(soup('div', 'page')[0].find_all('a')[-1]['href'].split('_')[1].split('.')[0])
        print(page_count)
        domain = 'http://dmqzjj.doumen.gov.cn/zlaq/jgys/index_%s.htm'
        for i in range(1, page_count + 1):
            link = domain % str(i)
            self.crawl(link, save=response.save, age=1, fetch_type='js',
                callback=self.build_list_page)

    def build_list_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        lists = soup('div', 'listr right')[0].find('ul').find_all('a', href=True)
        print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save=response.save, callback=self.content_page, fetch_type='js')

    def land_page(self, response):
        # 获取总页数
        page_tag = response.doc('#pagesplit > table > tbody > tr')
        tag_text = page_tag.text()
        p1 = tag_text.find('共')
        p2 = tag_text.rfind(' 页')
        page_count = int(tag_text[p1+2:p2])
        print(page_count)
        # 获取当前页数
        path,params = response.url.split('?')
        param = params.split('&')
        for each in param:
            if 'Page' in each:
                current_page=int(each[5:])
        print(current_page)
        # 这是目录页
        if current_page < page_count:
            if(response.save['flag']==1):
                url = 'http://www.gtjzh.gov.cn/gtj/list.asp?id=56&Page=' + str(current_page+1)
                self.crawl(url, age=1, save=response.save, 
                    callback=self.land_page, fetch_type='js')
            if(response.save['flag']==2):
                url = 'http://www.gtjzh.gov.cn/gtj/list.asp?id=57&Page=' + str(current_page+1)
                self.crawl(url, age=1, save=response.save, 
                    callback=self.land_page, fetch_type='js')
                
        for each in response.doc('#cbox > div.newslistbox > li').items():
            self.crawl(each.children('a').attr.href, age=1, 
                save=response.save,
                callback=self.content_page, fetch_type='js')    
                              
    def plan_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', {'class':'listFoot'})[0].find_all('a')[-1]['href'].split('&')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.plan_list_page, age=1, save=response.save)

        lists = soup('table')[2].find_all('a')
        domain = 'http://www.zhzgj.gov.cn/'
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table')[2].find_all('a')
        domain = 'http://www.zhzgj.gov.cn/'
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save) 