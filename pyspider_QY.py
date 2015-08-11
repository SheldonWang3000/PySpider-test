from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''清远'''

class Handler(My):
    name = "QY"

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_site_submission&page=1', 
            callback=self.plan_page, force_update=True, 
            save={'type':self.table_name[0], 'source':'GH'})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=businesses_project_planning_permit&page=1', 
            callback=self.plan_page, force_update=True, 
            save={'type':self.table_name[1], 'source':'GH'})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_planning_permit&page=1', 
            callback=self.plan_page, force_update=True, 
            save={'type':self.table_name[2], 'source':'GH'})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=village_project_planning_permit&page=1', 
            callback=self.plan_page, force_update=True, 
            save={'type':self.table_name[3], 'source':'GH'})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_planning_acceptance&page=1', 
            callback=self.plan_page, force_update=True, 
            save={'type':self.table_name[4], 'source':'GH'})

        headers = {}
        headers['Accept'] = '*/*'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Connection'] = 'keep-alive'
        headers['Content-Length'] = '0'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Cookie'] = 'ASPSESSIONIDCCCTQBBA=KCNANNLDOIMECFJAIMCKNCMM; yunsuo_session_verify=e4ecb63e6f67da8abe8de0110ba17341; _gscu_1015059567=39174433vyrf0j32; _gscs_1015059567=t39208734md7nxq29|pv:2; _gscbrs_1015059567=1; Hm_lvt_872f2242082cb9b1f8ab105d4703b206=1439174433; Hm_lpvt_872f2242082cb9b1f8ab105d4703b206=1439208737'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        headers['Origin'] = 'http://www.qyggzyjy.com'
        headers['RA-Sid'] = '6FA100BB-20150228-025839-140a2d-0496ae'
        headers['RA-Ver'] = '3.0.7'
        headers['Referer'] = 'http://www.qyggzyjy.com/Item/list.asp?id=1514'
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        self.crawl('http://www.qyggzyjy.com/item/ajaxpage.asp?labelid=20127957470240&infoid=&classid=20138907766269&refreshtype=Folder&specialid=&curpage=1&id=1514', 
            callback=self.land_page, method='POST', data='', headers=headers,
            save={'type':self.table_name[14], 'source':'GH'}, fetch_type='js', force_update=True)

    def plan_page(self, response):
        r = BeautifulSoup(response.text)
        page_count = int(r('table', {'class':'p-table'})[0].find_all('td')[0].get_text().split('\n')[1][5:])
        per_page = int(r('table', {'class':'p-table'})[0].find_all('td')[0].get_text().split('\n')[2][:-5])
        pages = int(page_count / per_page) if page_count % per_page == 0 else int(page_count / per_page) + 1
        print(pages)
        url = response.url[:-1]
        for i in range(2, pages + 1):
            link = url + str(i)
            self.crawl(link, callback=self.plan_list_page, 
                force_update=True, save=response.save)

        domain = 'http://120.81.224.155:8084/project/show.php?id=%s&typeform=%s'
        lists = r('ul', {'class':'list'})[0].find_all('li')[1:]
        for i in lists:
            key = i.a['onclick']
            key = key[8:len(key) - 1]
            keys = key.split(',')
            request_id = keys[0]
            request_method = keys[1]
            request_method = request_method[1:len(request_method) - 1]
            link = domain % (request_id, request_method)
            # print link
            self.crawl(link, callback=self.content_page, save=response.save)

    def plan_list_page(self, response):
        r = BeautifulSoup(response.text)
        domain = 'http://120.81.224.155:8084/project/show.php?id=%s&typeform=%s'
        lists = r('ul', {'class':'list'})[0].find_all('li')[1:]
        for i in lists:
            key = i.a['onclick']
            key = key[8:len(key) - 1]
            keys = key.split(',')
            request_id = keys[0]
            request_method = keys[1]
            request_method = request_method[1:len(request_method) - 1]
            link = domain % (request_id, request_method)
            self.crawl(link, callback=self.content_page, save=response.save) 

    def land_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)

        url, params_str = response.url.split('?')
        params = {}
        for i in params_str.split('&'):
            temp = i.split('=')
            params[temp[0]] = temp[1]

        headers = {}
        headers['Accept'] = '*/*'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Connection'] = 'keep-alive'
        headers['Content-Length'] = '0'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Cookie'] = 'ASPSESSIONIDCCCTQBBA=KCNANNLDOIMECFJAIMCKNCMM; yunsuo_session_verify=e4ecb63e6f67da8abe8de0110ba17341; _gscu_1015059567=39174433vyrf0j32; _gscs_1015059567=t39208734md7nxq29|pv:2; _gscbrs_1015059567=1; Hm_lvt_872f2242082cb9b1f8ab105d4703b206=1439174433; Hm_lpvt_872f2242082cb9b1f8ab105d4703b206=1439208737'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        headers['Origin'] = 'http://www.qyggzyjy.com'
        headers['RA-Sid'] = '6FA100BB-20150228-025839-140a2d-0496ae'
        headers['RA-Ver'] = '3.0.7'
        headers['Referer'] = 'http://www.qyggzyjy.com/Item/list.asp?id=1514'
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
        headers['X-Requested-With'] = 'XMLHttpRequest'

        page_count = int(soup('a', {'id','prev'})[-1]['href'].split('(')[1].split(')')[0])
        for i in range(2, page_count + 1):
            params['curpage'] = str(i)
            self.crawl(url, params=params, data='', headers=headers, force_update=True,
                save=response.save, method='POST', fetch_type='js', callback=self.land_list_page)

    def land_list_page(self, response):
        soup = BeautifulSoup(response.text)
        lists = soup('table')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, callback=self.content_page, save=response.save)