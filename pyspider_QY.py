from pyspider.libs.base_handler import *
from my import My
from bs4 import BeautifulSoup

'''清远'''

class Handler(My):
    name = "QY"
    mkdir = '/home/sheldon/web/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_site_submission&page=1', 
            callback=self.index_page, save={'type':self.table_name[0]})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=businesses_project_planning_permit&page=1', 
            callback=self.index_page, save={'type':self.table_name[1]})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_planning_permit&page=1', 
            callback=self.index_page, save={'type':self.table_name[2]})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=village_project_planning_permit&page=1', 
            callback=self.index_page, save={'type':self.table_name[3]})
        self.crawl('http://120.81.224.155:8084/project/fany.php?typeform=project_planning_acceptance&page=1', 
            callback=self.index_page, save={'type':self.table_name[4]})

    def index_page(self, response):
        r = BeautifulSoup(response.text)
        page_count = int(r('table', {'class':'p-table'})[0].find_all('td')[0].get_text().split('\n')[1][5:])
        per_page = int(r('table', {'class':'p-table'})[0].find_all('td')[0].get_text().split('\n')[2][:-5])
        pages = int(page_count / per_page) if page_count % per_page == 0 else int(page_count / per_page) + 1
        print(pages)
        url = response.url[:-1]
        for i in range(2, pages + 1):
            link = url + str(i)
            self.crawl(link, callback=self.next_list, save=response.save)

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

    @config(priority=2)
    def next_list(self, response):
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