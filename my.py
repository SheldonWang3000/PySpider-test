from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import cx_Oracle
import hashlib
import time
import re
import os
import redis
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import quote
'''放到/opt/pythontools下'''
class My(BaseHandler):

    mkdir = '/home/oracle/Gis/'
    r = redis.Redis()
    download_key = 'download'
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  

    table_name = ['选址意见书', '建设用地规划许可证', '建设工程规划许可证', '乡村建设规划许可证',
                '规划验收合格证', '规划验收合格证', '批前公示', '批后公布', 'Unknow', '选址意见书_批前',
                '建设用地规划许可证_批前', '建设工程规划许可证_批前', '乡村建设规划许可证_批前',
                '规划验收合格证_批前', '挂牌', '竣工验收']

    city_name = {'CZ':'潮州', 'DG':'东莞', 'FS':'佛山', 'GZ':'广州', 'HY':'河源', 'HZ':'惠州', 
                 'JM':'江门', 'JM_X':'江门', 'JY':'揭阳', 'MM':'茂名', 'MZ':'梅州', 'QY':'清远', 
                 'SG':'韶关', 'ST':'汕头', 'SW':'汕尾', 'SZ':'深圳', 'YF':'云浮', 'YJ':'阳江', 
                 'ZH':'珠海', 'ZJ':'湛江', 'ZQ':'肇庆', 'ZS':'中山',
                 }

    source_name = {'GH':'规划', 'GT':'国土', 'JS':'建设', 'JT':'交通', 'GF':'公服'}

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
    }
    crawl_config = {
        "headers" : headers,
        "timeout" : 100
    }
    def on_start(self):
        print('请重新启动pyspider')
        pass

    # def index_page(self, response):
    #     pass

    # def next_list(self, response):
    #     pass

    def get_date(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    '''返回基本url和url参数'''
    def get_params(self, response=None, link=''):
        if response == None and not link:
            raise KeyError
        if response != None:
            url, params_str = response.url.split('?')
        else:
            url, params_str = link.split('?')
        params = {}
        for i in params_str.split('&'):
            temp = i.split('=')
            params[temp[0]] = temp[1]
        return (url, params)

    '''生成绝对链接'''
    def real_path(self, a, b):
        path = urljoin(a, b)
        arr = urlparse(path)
        real_path = os.path.normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, real_path, arr.params, arr.query, arr.fragment))

    # def js_css_download(self, response):
    #     # 存储位置
    #     path = response.save['path']
    #     file_name = response.save['name']
    #     # 创建目录
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     with open(path + file_name, 'w') as f:
    #         f.write(response.text)

    @config(priority=2)
    def content_page(self, response):
        '''构造存储位置'''
        url = response.url
        m = hashlib.md5()
        m.update(url.encode())
        web_name = '/' + m.hexdigest() + '/'
        path = self.mkdir + self.name + '/' + response.save['source'] + '/' +  web_name
        if not os.path.exists(path):
            os.makedirs(path)        

        soup = BeautifulSoup(response.text)
        '''提取js文件'''
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
            d = {}
            d['url'] = request_url
            d['type'] = 'attachment'
            d['path'] = path
            d['file_name'] = each['src']
            self.r.rpush(self.download_key, str(d))
            # self.crawl(request_url, fetch_type='js', callback = self.js_css_download, save = {'path':path, 'name':each['src']})
        '''提取css文件'''
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
            d = {}
            d['url'] = request_url
            d['type'] = 'attachment'
            d['path'] = path
            d['file_name'] = each['href']
            self.r.rpush(self.download_key, str(d))
            # self.crawl(request_url, callback = self.js_css_download, save = {'path':path, 'name':each['href']})
        '''提取图片，显示用的img标签内的文字'''
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
                    d['file_name'] = each['src']
                    self.r.rpush(self.download_key, str(d))
        '''提取附件'''            
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
                       d['file_name'] = each['href']
                       self.r.rpush(self.download_key, str(d))
        '''提取background图片'''
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
                d['file_name'] = each['src']
                self.r.rpush(self.download_key, str(d))

        return {
            "url": url,
            "html": str(soup),
            "type": response.save['type'],
            "source": response.save['source']
        }


    def on_result(self, result):
        if result is not None: 
            m = hashlib.md5()
            m.update(result['url'].encode())
            web_name = '/' + m.hexdigest() + '/'
            path = self.mkdir + self.name + '/' +  result['source'] + '/' + web_name
            if not os.path.exists(path):
                os.makedirs(path)           

            page_path = path + 'page.html'
            f = open(page_path, 'wb')
            f.write(result['html'].encode('utf-8'))
            f.close()
            '''去除页面全部标签，只获得全部文字，用于全文索引'''
            content_path = path + 'content.txt'
            soup = BeautifulSoup(result['html'], 'html.parser')
            for i in soup('style') + soup('script'):
                i.extract()
            content = soup.decode('utf-8')
            content = re.sub(r'<[/!]?\w+[^>]*>', '\n', content)
            content = re.sub(r'<!--[\w\W\r\n]*?-->', '\n', content)
            content = re.sub(r'\s+', '\n', content)

            print(self.get_date())
            values = (result['url'], path,
                    self.get_date(), self.city_name[self.name], 
                    result['type'], content, result['source'])
            '''存入数据库'''
            conn = None
            try:
                dsn = cx_Oracle.makedsn('localhost', 1521, 'urbandeve')
                conn = cx_Oracle.connect(user='C##WWPA', password='wwpa5678', dsn=dsn)
                try:
                    cursor = conn.cursor()
                    cursor.setinputsizes(cx_Oracle.NCHAR, cx_Oracle.NCHAR,
                        cx_Oracle.DATETIME, cx_Oracle.NCHAR,
                        cx_Oracle.NCHAR, cx_Oracle.CLOB, cx_Oracle.NCHAR)
                    cursor.prepare('''insert into TBL_ORGLPBLC 
                        (ORIGINALADDRESS, STORAGEPATH, 
                        ARCHIVEDATE, ASCRIPTIONCITY, DOCUMENTTYPE, BODY, SOURCE) 
                        values(:1, :2, to_date(:3, 'yyyy-mm-dd'), :4, :5, :6, :7)''')
                    cursor.execute(None, values)
                    conn.commit()
                finally:
                    cursor.close()
            finally:
                if conn is not None:
                    conn.close()


        super(My, self).on_result(result)