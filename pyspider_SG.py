from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup
import hashlib
import re
import os
from urllib.parse import quote
'''韶关'''

class Handler(My):
    name = "SG"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.sggh.gov.cn/Article_Class_Item.asp?ClassID=148&ChildClassID=219&page=1', 
            callback=self.approval_page, age=1, 
            save={'type':self.table_name[8], 'source':'GH'})
        self.crawl('http://www.sggh.gov.cn/article_Class_Item.asp?ClassID=148&ChildClassID=204&page=1', 
            callback=self.approval_page, age=1, 
            save={'type':self.table_name[8], 'source':'GH'})

        self.crawl('http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!deptgovp_list.action?deptId=547&titleTypeId=605&siteOrgCode=440200&pagesize=15&action=show&pager.offset=0&currentpage=1&pagesize=15', 
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!deptgovp_list.action?deptId=547&titleTypeId=606&siteOrgCode=440200&pagesize=15&action=show&pager.offset=0&currentpage=1&pagesize=15', 
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!deptgovp_list.action?deptId=547&titleTypeId=607&siteOrgCode=440200&pagesize=15&action=show&pager.offset=0&currentpage=1&pagesize=15', 
            callback=self.certificate_page, age=1, 
            save={'type':self.table_name[2], 'source':'GH'})

        self.crawl('http://www.sgland.gov.cn/ggxx.asp?page=1', callback=self.land_page,
            save={'type':self.table_name[14], 'source':'GT'}, age=1, fetch_type='js')

    def approval_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('a', {'href':re.compile(r'Article_Class')})[-1]['href'].split('&')[-1].split('=')[-1])

        url = response.url[:-1]
        for i in range(2, page_count + 1):
            link = url + str(i)
            self.crawl(link, callback=self.approval_list_page, 
                age=1, save=response.save)

        lists = soup('ul')[2].find_all('li')
        domain = 'http://www.sggh.gov.cn/'
        for i in lists:
            link = domain + i.find('a')['href']
            self.crawl(link, fetch_type='js', callback=self.approval_content_page, save=response.save)
            
    def certificate_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('div', 'list_page')[0].find('table').find_all('a')[-1]['onclick'].split(',')[1].strip('\''))

        url = response.url
        params_str = url.split('?')[1].split('&')
        params = {}
        for i in params_str:
            if len(i) != 0:
                temp = i.split('=') 
                params[temp[0]] = temp[1]

        for i in range(2, page_count + 1):
            link = url.split('?')[0]
            params['currentpage'] = str(i)
            self.crawl(link, callback=self.certificate_list, age=1, 
                params=params, save=response.save)

        lists = soup('table', 'service_table')[0].find_all('a')
        domain = 'http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!single.action'
        for i in lists:
            params_list = i['onclick'].split('(')[1].split(')')[0].split(',')
            params_list = [j.strip('\'') for j in params_list]
            params = {}
            params['deptId'] = params_list[0] 
            params['filePath'] = params_list[1]
            self.crawl(domain, fetch_type='js', params=params, 
                callback=self.iframe_page, save=response.save)

    def land_page(self, response):
        soup = BeautifulSoup(response.text)
        page_count = int(soup('span', 'news_text')[-1].find_all('strong')[1].get_text())

        url, params = self.get_params(response)
        for i in range(2, page_count + 1):
            params['page'] = str(i)
            self.crawl(url, params=params, save=response.save, fetch_type='js',
                age=1, callback=self.land_list_page)

        lists = soup('table', 'dh')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, 
                save=response.save, fetch_type='js')


    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table', 'dh')[0].find_all('a', {'target':'_blank'})
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, 
                save=response.save, fetch_type='js')

    def iframe_page(self, response):
        soup = BeautifulSoup(response.text)
        iframe = soup('iframe')[1]
        link = self.real_path('http://zwgk.sg.gov.cn/', iframe['src'])
        self.crawl(link, fetch_type='js', save=response.save, callback=self.content_page)

    def certificate_list(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table', 'service_table')[0].find_all('a')
        domain = 'http://zwgk.sg.gov.cn/website/govPublic/govPublicSiteAction!single.action'
        for i in lists:
            params_list = i['onclick'].split('(')[1].split(')')[0].split(',')
            params_list = [j.strip('\'') for j in params_list]
            params = {}
            params['deptId'] = params_list[0] 
            params['filePath'] = params_list[1]
            self.crawl(domain, fetch_type='js', params=params, 
                callback=self.iframe_page, save=response.save)

    def approval_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('ul')[2].find_all('li')
        domain = 'http://www.sggh.gov.cn/'
        for i in lists:
            link = domain + i.find('a')['href']
            self.crawl(link, fetch_type='js', callback=self.approval_content_page, save=response.save)

    def approval_content_page(self, response):
        url = response.url
        m = hashlib.md5()
        m.update(url.encode())
        web_name = '/' + m.hexdigest() + '/'
        path = self.mkdir + self.name + web_name
        if not os.path.exists(path):
            os.makedirs(path)           

        soup = BeautifulSoup(response.text)

        script_tag = soup.find_all('script', src=True)
        for each in script_tag:
            js_m = hashlib.md5()
            js_m.update(each['src'].encode())
            js_name = js_m.hexdigest()
            # 获取访问地址
            request_url = self.real_path(url, each['src'])
            # 改动网页 css 地址为相对地址
            each['src'] = js_name + '.js'
            # 爬取css文件
            self.crawl(request_url, fetch_type='js', callback = self.js_css_download, save = {'path':path, 'name':each['src']})

        css_tag = soup.find_all('link', type='text/css')
        for each in css_tag:
            css_m = hashlib.md5()
            css_m.update(each['href'].encode())
            css_name = css_m.hexdigest()
            # 获取访问地址
            request_url = self.real_path(url, each['href'])
            # 改动网页 css 地址为相对地址
            each['href'] = css_name + '.css'
            # 爬取css文件
            self.crawl(request_url, callback = self.js_css_download, save = {'path':path, 'name':each['href']})

        images = soup('img')
        image_list = []
        if images is not None:
            for each in images:
                image_url = self.real_path(url, each['src'])
                k = image_url.split('/')
                link = k[0]
                for i in k[1:]:
                    link += '/'+ quote(i)
                image_url = link
                if image_url not in image_list:
                    # t = re.search('.asp', image_url)
                    # if t is None:
                    image_list.append(image_url)
                    d = {}
                    d['type'] = 'image'
                    d['path'] = path
                    d['url'] = image_url
                    m = hashlib.md5()
                    m.update(image_url.encode())
                    if re.search('.jpg', image_url) is not None:
                        each['src'] = m.hexdigest() + '.jpg'
                    elif re.search('.png', image_url) is not None:
                        each['src'] = m.hexdigest() + '.png'
                    elif re.search('.gif', image_url) is not None:
                        each['src'] = m.hexdigest() + '.gif'
                    d['name'] = each['src']
                    self.r.rpush(self.download_key, str(d))

        attachments = soup('a', {'href': re.compile(r'^http')})
        attachment_list = []
        if attachments is not None:
            for each in attachments:
                href = each['href']
                type_name = None
                if re.search('.jpg', href) is not None:
                    type_name = 'jpg'
                elif re.search('.png', href) is not None:
                    type_name = '.png'
                elif re.search('.gif', href) is not None:
                    type_name = '.gif'
                elif re.search('.doc', href) is not None:
                    type_name = '.doc'
                elif re.search('.pdf', href) is not None:
                    type_name = '.pdf'
                elif re.search('.zip', href) is not None:
                    type_name = '.zip'
                elif re.search('.rar', href) is not None:
                    type_name = '.rar'
                if type_name is not None:
                    attachment_url = self.real_path(url, href)
                    k = attachment_url.split('/')
                    link = k[0]
                    for i in k[1:]:
                        link += '/'+ quote(i)
                    attachment_url = link
                    if attachment_url not in attachment_list and attachment_url not in image_list:
                       attachment_list.append(href)
                       d = {}
                       d['type'] = 'attachment'
                       d['path'] = path
                       d['url'] = attachment_url
                       m = hashlib.md5()
                       m.update(attachment_url.encode())
                       each['href'] = m.hexdigest() + '.' + type_name
                       d['name'] = each['href']
                       self.r.rpush(self.download_key, str(d))

        # 针对 background 属性
        for key in soup.find_all(background=True):
            image_url = self.real_path(url, key['background'])
            k = image_url.split('/')
            link = k[0]
            for i in k[1:]:
                link += '/'+ quote(i)
            image_url = link
            if image_url not in image_list:
                image_list.append(image_url)
                d = {}
                d['type'] = 'image'
                d['path'] = path
                d['url'] = image_url
                m = hashlib.md5()
                m.update(image_url.encode())
                if re.search('.jpg', image_url) is not None:
                    each['src'] = m.hexdigest() + '.jpg'
                elif re.search('.png', image_url) is not None:
                    each['src'] = m.hexdigest() + '.png'
                elif re.search('.gif', image_url) is not None:
                    each['src'] = m.hexdigest() + '.gif'
                d['name'] = each['src']
                self.r.rpush(self.download_key, str(d))

        images = soup('iframe')
        if images is not None:
            for each in images:
                src = each['src']
                params = src.split('&')
                data = {}
                for i in params:
                    temp = i.split('=')
                    data[temp[0]] = temp[1]
                image_url = self.real_path(url, data['uf'])
                k = image_url.split('/')
                link = k[0]
                for i in k[1:]:
                    link += '/'+ quote(i)
                image_url = link
                if image_url not in image_list:
                    image_list.append(image_url)
                    d = {}
                    d['type'] = 'image'
                    d['path'] = path
                    d['url'] = image_url
                    m = hashlib.md5()
                    m.update(image_url.encode())
                    if re.search('.jpg', image_url) is not None:
                        each['src'] = m.hexdigest() + '.jpg'
                    elif re.search('.png', image_url) is not None:
                        each['src'] = m.hexdigest() + '.png'
                    elif re.search('.gif', image_url) is not None:
                        each['src'] = m.hexdigest() + '.gif'
                    d['name'] = each['src']
                    self.r.rpush(self.download_key, str(d))

        return {
            "url": url,
            "html": str(soup),
            "type": response.save['type']
        }