from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import re
import xmltodict
from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.parse import quote
'''东莞'''

class Handler(My):
    name = "DG"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9&page=1', 
            fetch_type='js', age=1, callback=self.plan_page, 
            save={'page':1, 'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%D3%C3%B5%D8%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&page=1', 
            fetch_type='js', age=1, callback=self.plan_page, 
            save={'page':1, 'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://121.10.6.230/dggsweb/SeePHAllGS.aspx?%B9%AB%CA%BE=%C5%FA%BA%F3%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%B9%A4%B3%CC%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&page=1', 
            fetch_type='js', age=1, callback=self.plan_page, 
            save={'page':1, 'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://121.10.6.230/dggsweb/SeePQAllGS.aspx?%B9%AB%CA%BE=%C5%FA%C7%B0%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9&page=1', 
            fetch_type='js', age=1, callback=self.plan_page, 
            save={'page':1, 'type':self.table_name[9], 'source':'GH'})
        self.crawl('http://121.10.6.230/dggsweb/SeePQAllGS.aspx?%B9%AB%CA%BE=%C5%FA%C7%B0%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%D3%C3%B5%D8%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&page=1', 
            fetch_type='js', age=1, callback=self.plan_page, 
            save={'page':1, 'type':self.table_name[10], 'source':'GH'})
        self.crawl('http://121.10.6.230/dggsweb/SeePQAllGS.aspx?%B9%AB%CA%BE=%C5%FA%C7%B0%B9%AB%CA%BE&%D2%B5%CE%F1%C0%E0%D0%CD=%BD%A8%C9%E8%B9%A4%B3%CC%B9%E6%BB%AE%D0%ED%BF%C9%D6%A4&page=1', 
            fetch_type='js', age=1, callback=self.plan_page, 
            save={'page':1, 'type':self.table_name[11], 'source':'GH'})

        self.crawl('http://land.dg.gov.cn/publicfiles/business/htmlfiles/gtj/s15867/list.htm',
            fetch_type='js', age=1, callback=self.land_page,
            save={'type':self.table_name[14], 'source':'GT'},
            js_script='''function(){return new XMLSerializer().serializeToString(_getPagefromArr('2').docObj);}''')
        self.crawl('http://land.dg.gov.cn/publicfiles/business/htmlfiles/gtj/s30308/list.htm',
            fetch_type='js', age=1, callback=self.land_page,
            save={'type':self.table_name[14], 'source':'GT'},
            js_script='''function(){return new XMLSerializer().serializeToString(_getPagefromArr('2').docObj);}''')
        self.crawl('http://land.dg.gov.cn/publicfiles/business/htmlfiles/gtj/s16089/list.htm',
            fetch_type='js', age=1, callback=self.land_page,
            save={'type':self.table_name[14], 'source':'GT'},
            js_script='''function(){return new XMLSerializer().serializeToString(_getPagefromArr('2').docObj);}''')

    def land_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        info = xmltodict.parse(response.js_script_result)
        lists = info['xml']['RECS']['INFO']
        domain = 'http://land.dg.gov.cn/publicfiles/business/htmlfiles/'
        for i in lists:
            link = self.real_path(domain, i['InfoURL'])
            print(link)
            if link.endswith('htm'):
                self.crawl(link, save=response.save, callback=self.content_page)


    def plan_page(self, response):
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
            temp = response.orig_url.split('&')
            url = temp[0]
            for i in temp[1:-1]:
                url += '&' + i
            print(url)
            url = url + '&' + str(response.save['page'] + 1)
            save_dict = response.save
            save_dict['page'] = save_dict['page'] + 1
            self.crawl(url, method='POST',
                data=data, callback=self.plan_page, age=1, save=save_dict)

        content = soup('a', {'target':'_blank'})

        domains = {}
        domains[self.table_name[0]] = 'http://121.10.6.230/dggsweb/PHGSFJ/PHjsxmxzFJ.aspx?'
        domains[self.table_name[1]] = 'http://121.10.6.230/dggsweb/PHGSFJ/PHjsydghFJ.aspx?'
        domains[self.table_name[2]] = 'http://121.10.6.230/dggsweb/PHGSFJ/PHjsgcghFJ.aspx?' 
        domains[self.table_name[9]] = 'http://121.10.6.230/dggsweb/PQGSFJ/PQszFJ.aspx?'
        domains[self.table_name[10]] = 'http://121.10.6.230/dggsweb/PQGSFJ/PQyslzFJ.aspx?'
        domains[self.table_name[11]] = 'http://121.10.6.230/dggsweb/PQGSFJ/PQyslzFJ.aspx?'

        for i in content:
            link = i['href']
            h = HTMLParser()
            link = h.unescape(link)
            parmas = link.split('?')[1]
            parmas = parmas.split('&')
            link = ''
            link += quote('项目受理编号'.encode('gbk')) + '=' + quote(parmas[0].split('=')[1].encode('gbk')) + '&' + quote('公示'.encode('gbk')) + '=' + quote(parmas[1].split('=')[1].encode('gbk'))
            domain = domains[response.save['type']]
            link = domain + link
            # print(link)
            self.crawl(link, callback=self.content_page, save={'type':response.save['type']})