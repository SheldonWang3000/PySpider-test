from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
from my import My
import re
from datetime import datetime as date

class Handler(My):
    name = 'DP'

    @every(minutes = 24 * 60)
    def on_start(self):
        self.crawl('http://www.dianping.com/search/category/4/10', age=1,
            save={'type':'food', 'source':'GZ'}, callback=self.index_page)

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'classfy'})[0].find_all('a')
        print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            # print(link)
            self.crawl(link, save=response.save, age=1, callback=self.classfy_page) 

    def classfy_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'region-nav'})[0].find_all('a')
        print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            link = link.split('#')[0]
            # print(link)
            self.crawl(link, save=response.save, age=1, callback=self.region_page) 

    def region_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'region-nav-sub'})[0].find_all('a')[1:]
        print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            link = link.split('#')[0]
            print(link)
            self.crawl(link, save=response.save, age=1, callback=self.list_page) 

    def list_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        next = soup('a','next')
        if len(next) != 0:
            link = self.real_path(response.url, next[0]['href'])
            self.crawl(link, age=1, save=response.save, callback=self.list_page)

        lists = soup('div', 'pic')
        shop_dict = {'food':self.food_shop_page}
        comment_dict = {'food':self.food_comment_page}
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, age=1, save=response.save, callback=shop_dict[response.save['type']])
            link += '/review_more'
            self.crawl(link, age=1, save=response.save, callback=comment_dict[response.save['type']])

    def food_shop_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        shop_no = response.url.split('/')[-1]
        d = {}
        d['shopNo'] = shop_no
        region = soup('span', {'itemprop':'locality region'})[0].get_text(strip=True)
        street = soup('span', {'itemprop':'street-address'})[0].get_text(strip=True)
        address = region + street
        d['address'] = address
        shop_name = soup('h1', 'shop-name')[0].get_text('|', strip=True)
        shop_name = shop_name.split('|')[0]
        d['shopName'] = shop_name
        values = soup('div', 'brief-info')[0].find_all('span', 'item')
        t = []
        d['commentsNum'] =values[0].get_text().split('条')[0]
        for i in values[1:]:
            s = i.get_text().split('：')[1]
            t.append(s)
        d['avg'] = t[0]
        d['taste'] = t[1]
        d['surroundings'] = t[2]
        d['service'] = t[3]
        print(d)
        return {
            'content':str(d),
            'type':'food_shop'
        }

    def food_comment_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        all_num = soup('span', 'active')[0].find('em').get_text().split('(')[1].split(')')[0]
        all_num = int(all_num)
        print(all_num)
        page_count = int(soup('div', 'Pages')[1].find_all('a')[-2]['title'])
        print(page_count)
        for i in range(2, page_count + 1):
            link = response.url + '?pageno=' + str(i)
            self.crawl(link, age=1, save=response.save, callback=self.food_comment_list_page)

        self.food_comment_page(response)

    def food_comment_list_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')        
        lists = soup('div', 'comment-list')[0].find_all('li')
        comments = []
        for i in lists:
            t = i.find('div', 'J_brief-cont')
            if t is not None:
                v = i.find('div', 'user-info').find_all('span')
                values = []
                values.append(v[0]['title'])
                for j in v[1:]:
                    if j['class'][0] == "comm-per":
                        print('jump')
                        continue
                    temp = j.em.get_text().split('(')[1].split(')')[0]
                    values.append(temp)
                like = i.find('div', 'comment-recommend')
                if like is not None:
                    like = like.find('a').get_text()
                time = i.find('span', 'time').get_text()
                content = t.get_text()
                if len(time.split('-')) < 3:
                    time = str(date.now().year)[2:] + '-' + time
                d = {}
                d['overview'] = values[0]
                d['taste'] = values[1]
                d['surroundings'] = values[2]
                d['service'] = values[3]
                d['like'] = like
                d['comment'] = content.strip()
                d['time'] = time
                comments.append(d)
                print(str(d))
                print('--------')

        return {
            'content':str(comments),
            'type':'food'
        }

    def on_result(self, result):
        if result is not None:
            content = eval(result['content'])
            print(len(content))