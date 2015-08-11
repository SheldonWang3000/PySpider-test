from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''云浮'''

class Handler(My):
    name = "YF"
    
    @every(minutes=24 * 60)
    def on_start(self):
        url = 'http://gtzy.yunfu.gov.cn/website/newdeptemps/gtzy/news.jsp?columnid=009001056011&ipage=1'
        # 爬取 url 网页，回调index_page 函数 ，页面类型为：1 目录页
        self.crawl(url, fetch_type='js', callback=self.index_page, 
            force_update=True, save={'page':1, 'type':self.table_name[8], 'source':'GH'})
        self.crawl('http://gtzy.yunfu.gov.cn/website/newdeptemps/gtzy/news.jsp?columnid=009001056008&ipage=1', fetch_type='js', callback=self.index_page, 
            force_update=True, save={'page':1, 'type':self.table_name[14], 'source':'GT'})

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        pagediv = soup.find('div',class_='fanyie').find_all('a')[-1]
        position = pagediv['href'].find('ipage=')
        params = {}
        for i in pagediv['href'].split('?')[-1].split('&'):
            temp = i.split('=')
            params[temp[0]] = temp[1]
        pageAllCount = int(params['ipage'])
        url = response.url[:-1]
        for i in range(2, pageAllCount + 1):
            link = url + str(i)
            self.crawl(link, fetch_type='js', force_update=True, 
                callback=self.next_list, save=response.save)

        contentPageList = []    
        lists = soup('ul', 'list4')[0].find_all('a', href=True)
        for li in lists:
            content_urltag = li
            position = content_urltag['href'].find('/is')
            pageUrl = content_urltag['href'][position:-3]
            # print(pageUrl)
            contentPageList.append(pageUrl)
        for uri in contentPageList:
            # 爬取内容页面
            self.crawl('http://gtzy.yunfu.gov.cn'+uri, callback=self.content_page, 
                save=response.save)
            
    def next_list(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        contentPageList = []    
        lists = soup('ul', 'list4')[0].find_all('a', href=True)
        for li in lists:
            content_urltag = li
            position = content_urltag['href'].find('/is')
            pageUrl = content_urltag['href'][position:-3]
            # print(pageUrl)
            contentPageList.append(pageUrl)
        for uri in contentPageList:
            # 爬取内容页面
            self.crawl('http://gtzy.yunfu.gov.cn'+ uri, callback=self.content_page, 
                save=response.save)