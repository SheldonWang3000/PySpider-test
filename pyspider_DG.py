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
'''东莞'''

class Handler(My):
    name = "DG"
    mkdir = '/home/sheldon/web/'
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9&1', 
            callback=self.index_page, save={'page':1, 'type':'项目选址意见书'})
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%D3%C3%B5%D8%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&1', 
            fetch_type='js', callback=self.index_page, save={'page':1, 'type':'用地规划许可证'})
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%B9%A4%B3%CC%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&1', 
            fetch_type='js', callback=self.index_page, save={'page':1, 'type':'工程规划许可证'})

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
      
        last_page = int(soup.find(id=re.compile(r'LabelPageCount')).get_text())
        if last_page != response.save['page']:
            parmas = {'__EVENTTARGET': 'GridView1$ctl23$LinkButtonNextPage',
            '__EVENTARGUMENT': '', 
            }
            parmas['__VIEWSTATE'] = soup.find('input', {'name': '__VIEWSTATE'})['value']
            parmas['__EVENTVALIDATION'] = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
            parmas['GridView1$ctl23$tbPage'] = str(response.save['page'])

            data = urlencode(parmas)
            print(response.orig_url)
            temp = response.orig_url.split('&')
            print(temp)
            # url = response.orig_url[:-2]
            url = temp[0]
            for i in temp[1:-1]:
                url += '&' + i
            print(url)
            url = url + '&' + str(response.save['page'] + 1)
            save_dict = response.save
            save_dict['page'] = save_dict['page'] + 1
            self.crawl(url, method='POST', data=data, callback=self.index_page, save=save_dict)

        content = response.doc('a[href^=http]')
        for i in content.items():
            link = i.attr.href
            h = HTMLParser()
            link = h.unescape(link)
            parmas = link.split('?')[1]
            parmas = parmas.split('&')
            link = ''
            link += quote('项目受理编号'.encode('gbk')) + '=' + quote(parmas[0].split('=')[1].encode('gbk')) + '&' + quote('公示'.encode('gbk')) + '=' + quote(parmas[1].split('=')[1].encode('gbk'))
            domain = 'http://121.10.6.230/dggsweb/PHGSFJ/PHjsxmxzFJ.aspx?'
            link = domain + link
            # print(link)
            self.crawl(link, callback=self.content_page, save = save_dict)