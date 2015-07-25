from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import quote
import redis
'''云浮'''

class Handler(My):
    name = "YF"
    mkdir = '/home/sheldon/web/'
    
    @every(minutes=24 * 60)
    def on_start(self):
        url = 'http://gtzy.yunfu.gov.cn/website/newdeptemps/gtzy/news.jsp?columnid=009001056011'
        # 爬取 url 网页，回调index_page 函数 ，页面类型为：1 目录页
        self.crawl(url, fetch_type='js', callback=self.index_page)

    def index_page(self, response):
        contentPageList = []
        if response.save == 1:
            # 计算总页数 pageAllCount
            soup = BeautifulSoup(response.text, 'html.parser')
            pagediv = soup.find('div',class_='fanyie').find_all('a')[-1]
            position = pagediv['href'].find('ipage=')
            pageAllCount = int(pagediv['href'][position+6:])
        
            # 计算当前页 currentPage
            request_url = response.url
            print(request_url)
            position = request_url.find('ipage=')
            if position == -1:
                currentPage = 1
            else:
                url = url[0:position-1]
                currentPage = int(response.url[position+6:])
            
            for li in soup.select('.newslist li'):
                content_urltag = li.find('a')
                position = content_urltag['href'].find('/is')
                pageUrl = content_urltag['href'][position:-3]
                print(pageUrl)
                contentPageList.append(pageUrl)
        
            if currentPage <= pageAllCount:
                # 爬取目录页面
                self.crawl(request_url, callback=self.index_page, method='GET',params={'ipage': currentPage + 1 },save=1)
                
            for uri in contentPageList:
                # 爬取内容页面
                self.crawl('http://gtzy.yunfu.gov.cn'+uri, callback=self.content_page)