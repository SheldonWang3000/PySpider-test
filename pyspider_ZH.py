from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''珠海'''

class Handler(My):
    name = "ZH"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%D2%B5%CE%F1%B9%AB%CA%BE&MdlName=%D3%C3%B5%D8%C0%E0%B9%AB%CA%BE&page=1', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[1]})
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%d2%b5%ce%f1%b9%ab%ca%be&MdlName=%bd%a8%d6%fe%b9%a4%b3%cc%b9%e6%bb%ae%b9%ab%ca%be&page=1', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[2]})
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%D2%B5%CE%F1%B9%AB%CA%BE&MdlName=%BD%BB%CD%A8%D3%EB%CA%D0%D5%FE%B9%A4%B3%CC%B9%E6%BB%AE%C0%E0&page=1', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[2]})
        self.crawl('http://www.zhzgj.gov.cn/WxList.aspx?WstName=%d2%b5%ce%f1%b9%ab%ca%be&MdlName=%b9%e6%bb%ae%cc%f5%bc%fe%ba%cb%ca%b5&page=1', 
            callback=self.index_page, force_update=True, save={'type':self.table_name[4]})

    def index_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', {'class':'listFoot'})[0].find_all('a')[-1]['href'].split('&')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list, force_update=True, save=response.save)

        lists = soup('table')[2].find_all('a')
        domain = 'http://www.zhzgj.gov.cn/'
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save)

    @config(priority=2)
    def next_list(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table')[2].find_all('a')
        domain = 'http://www.zhzgj.gov.cn/'
        for i in lists:
            link = domain + i['href']
            self.crawl(link, callback=self.content_page, save=response.save) 