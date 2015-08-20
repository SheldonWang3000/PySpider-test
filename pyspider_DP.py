from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
from my import My
import re
import cx_Oracle
import time
from datetime import datetime as date

class Handler(My):
    name = 'DP'

    @every(minutes = 24 * 60)
    def on_start(self):
        self.crawl('http://www.dianping.com/search/category/4/10', age=1,
            save={'type':'food', 'source':'GZ'}, callback=self.index_page)

        self.crawl('http://www.dianping.com/guangzhou/hotel', age=1,
            save={'source':'GZ'}, callback=self.hotel_index_page)

    def hotel_index_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', 'nav-2nd J_choice-trigger-wrap-downtown')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, age=1, callback=self.hotel_street_page)

        lists = soup('div', 'J_choice-content choice-wrap gray ')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save={'type':'hot'}, age=1, callback=self.hotel_location_page)

        lists = soup('div', 'nav-2nd J_choice-trigger-wrap-metro')[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, age=1, callback=self.hotel_metro_page)

    def hotel_metro_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', 'recom J_choice-content-2nd ')[0].find_all('a')[1:]
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, save={'type':'metro'}, age=1, callback=self.hotel_location_page)

    def hotel_location_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        next = soup('a','next')
        if len(next) != 0:
            link = self.real_path(response.url, next[0]['href'])
            self.crawl(link, age=1, save=response.save, callback=self.hotel_location_page)

        lists = soup('a', 'hotel-name-link')
        if response.save['type'] == 'hot':
            t = soup('div', 'J_choice-content choice-wrap gray ')[0].find('a', 'cur')
            message = t.get_text() 
        else:
            t = soup('div', 'nav-2nd J_choice-trigger-wrap-metro')[0].find('a', 'J_choice-trigger-2nd cur')
            message = t.get_text()
            t = soup('div', 'recom J_choice-content-2nd ')[0].find('a', 'cur')
            message += ' ' + t.get_text()
        t = []
        for i in lists:
            d = {}
            d['shopNo'] = i['href'].split('/')[-1]
            d['message'] = message
            t.append(d)
        print(t)
        return {
            'content':str(t),
            'type':response.save['type'],
            'method':'location'
        }

    def hotel_street_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', 'recom J_choice-content-2nd ')[0].find_all('a')[1:]
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, age=1, callback=self.hotel_list_page)

    def hotel_list_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        next = soup('a','next')
        if len(next) != 0:
            link = self.real_path(response.url, next[0]['href'])
            self.crawl(link, age=1, callback=self.hotel_list_page)

        lists = soup('a', 'hotel-name-link')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            self.crawl(link, age=1, callback=self.hotel_page)
            link += '/review_more'
            self.crawl(link, age=1, callback=self.comment_page)

    def hotel_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        d = {}
        d['city'] = response.save['source']
        d['shopName'] = ''
        d['commentsNum'] = ''
        d['address'] = ''
        d['overview'] = ''
        shop_name = soup('h1', 'shop-name')[0].get_text().split('\n')[0]
        d['shopName'] = shop_name
        info = soup('p', 'info shop-star')[0].find_all('span')
        d['overview'] = str(int(info[0]['class'][1].split('str')[1]) / 10)
        d['commentsNum'] = re.findall(r'\d+', info[1].get_text())[0]
        address = ''.join(soup('p', 'shop-address')[0].get_text().split('\n')[0].split('：')[1].split('\xa0'))
        d['address'] = address
        print(d)
        return {
            'content':str(d),
            'type':'hotel',
            'method':'database'
        }

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'classfy'})[0].find_all('a')
        print(len(lists))
        for i in lists:
            link = self.real_path(response.url, i['href'])
            # print(link)
            self.crawl(link, save=response.save, age=1, callback=self.region_page) 

    def region_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'region-nav'})[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href'])
            link = link.split('#')[0]
            # print(link)
            self.crawl(link, save=response.save, age=1, callback=self.street_page) 

        lists = soup('div', {'id':'bussi-nav'})[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href']).split('#')[0]
            self.crawl(link, age=1, callback=self.shop_hot_page)

        lists = soup('div', {'id':'metro-nav'})[0].find_all('a')
        for i in lists:
            link = self.real_path(response.url, i['href']).split('#')[0]
            self.crawl(link, age=1, callback=self.shop_metro_page)

    def shop_metro_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'metro-nav-sub'})[0].find_all('a')[1:]
        for i in lists:
            link = self.real_path(response.url, i['href']).split('#')[0]
            self.crawl(link, age=1, save={'type':'metro'}, callback=self.shop_location_page)

    def shop_hot_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        lists = soup('div', {'id':'bussi-nav-sub'})[0].find_all('a')[1:]
        for i in lists:
            link = self.real_path(response.url, i['href']).split('#')[0]
            self.crawl(link, age=1, save={'type':'hot'}, callback=self.shop_location_page)

    def shop_location_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        next = soup('a','next')
        if len(next) != 0:
            link = self.real_path(response.url, next[0]['href'])
            self.crawl(link, age=1, save=response.save, callback=self.shop_location_page)

        lists = soup('div', 'pic')
        if response.save['type'] == 'hot':
            t = soup('div', {'id':'bussi-nav'})[0].find('a', 'cur')
            message = t.get_text() 
            t = soup('div', {'id':'bussi-nav-sub'})[0].find('a', 'cur')
            message += ' ' + t.get_text()
        else:
            t = soup('div', {'id':'metro-nav'})[0].find('a', 'cur')
            message = t.get_text()
            t = soup('div', {'id':'metro-nav-sub'})[0].find('a', 'cur')
            message += ' ' + t.get_text()
        t = []
        for i in lists:
            d = {}
            d['shopNo'] = i.a['href'].split('/')[-1]
            d['message'] = message
            t.append(d)
        print(t)
        return {
            'content':str(t),
            'type':response.save['type'],
            'method':'location'
        }

    def street_page(self, response):
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
        for i in lists:
            link = self.real_path(response.url, i.find('a')['href'])
            self.crawl(link, age=1, save=response.save, callback=self.shop_page)
            link += '/review_more'
            self.crawl(link, age=1, save=response.save, callback=self.comment_page)

    def shop_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        shop_no = response.url.split('/')[-1]
        d = {}
        d['shopNo'] = ''
        d['address'] = ''
        d['shopName'] = ''
        d['commentsNum'] = ''
        d['overview'] = ''
        d['avg'] = ''
        d['params1'] = ''
        d['params2'] = ''
        d['params3'] = ''
        d['city'] = response.save['source']
        # tags = soup('p', 'info info-indent')[1].find_all('a')
        # tag = '|'.join([i.get_text() for i in tags]) 
        # d['tag'] = tag
        d['shopNo'] = shop_no
        try:
            region = soup('span', {'itemprop':'locality region'})[0].get_text(strip=True)
            street = soup('span', {'itemprop':'street-address'})[0].get_text(strip=True)
            address = region + street
            d['address'] = address
            shop_name = soup('h1', 'shop-name')[0].get_text('|', strip=True)
            shop_name = shop_name.split('|')[0]
            d['shopName'] = shop_name
            values = soup('div', 'brief-info')[0].find_all('span', 'item')
            overview = soup('div', 'brief-info')[0].find('span')['class']
            d['overview'] = str(int(overview[1].split('str')[1]) / 10)
            d['commentsNum'] = values[0].get_text().split('条')[0]
            print('avg:' + values[1].get_text())
            temp = re.findall(r'\d+', values[1].get_text())
            print('aaaaa:' + temp)
            if len(temp) == 1:
                d['avg'] = temp[0]
            for index, i in enumerate(values[2:]):
                s = i.get_text()
                name = 'params' + str(index + 1)
                d[name] = s
        except IndexError:
            shop_name = soup('h2', 'market-name')[0].get_text()
            d['shopName'] = shop_name
            address = soup('div', 'market-detail')[0].find('p').get_text()
            address = ''.join(address.split('\n')[2:-1])
            address = ''.join(address.split(' '))
            d['address'] = address
            for index, i in enumerate(soup('div', 'market-detail-other')[0].find_all('p')[2].find_all('span')[2:]):
                name = 'params' + str(index + 1)
                d[name] = i.get_text()
            overview = soup('div', 'market-detail-other')[0].find_all('p')[2].find_all('span')[1]['class']
            overview = str(int(overview[1].split('str')[1]) / 10)
            d['overview'] = overview
            avg = re.findall(r'\d+', soup('div', 'market-detail-other')[0].find_all('p')[3].get_text())
            if len(avg) == 1:
                d['avg'] = avg[0]
            commentsNum = soup('a', {'data-type':'all'})[0].find('span').get_text()
            commentsNum = re.findall(r'\d+', commentsNum)[0]
            d['commentsNum'] = commentsNum
        print(d)
        return {
            'content':str(d),
            'type':response.save['type'],
            'method':'database'
        }

    def comment_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        shop_no = re.findall(r'\d+', response.url)[0]
        print(shop_no)
        all_num = soup('span', 'active')[0].find('em').get_text().split('(')[1].split(')')[0]
        all_num = int(all_num)
        print(all_num)
        if all_num <= 20:
            page_count = 1
        else:
            page_count = int(soup('div', 'Pages')[1].find_all('a')[-2]['title'])
        print(page_count)
        for i in range(2, page_count + 1):
            link = response.url + '?pageno=' + str(i)
            self.crawl(link, age=1, save=response.save, callback=self.comment_list_page)

        lists = soup('div', 'comment-list')[0].find_all('li')
        comments = []
        for i in lists:
            t = i.find('div', 'J_brief-cont')
            if t is not None:
                d = {}
                d['shopNo'] = ''
                d['overview'] = ''
                d['params1'] = ''
                d['params2'] = ''
                d['params3'] = ''
                d['comment'] = ''
                d['time'] = ''
                d['shopNo'] = shop_no
                v = i.find('div', 'user-info').find_all('span')
                d['overview'] = str(int(v[0]['class'][1].split('star')[1]) / 10)
                index = 1
                for j in v[1:]:
                    if j['class'][0] == "comm-per":
                        print('jump')
                        continue
                    name = 'params' + str(index)
                    index += 1
                    d[name] = j.get_text()
                # like = i.find('div', 'comment-recommend')
                # if like is not None:
                #     like = like.find('a').get_text()
                time = i.find('span', 'time').get_text().split('\xa0\xa0')[0]
                content = t.get_text()
                if len(time.split('-')) < 3:
                    time = str(date.now().year)[2:] + '-' + time
                # d['like'] = like
                d['comment'] = content.strip()
                d['time'] = time
                comments.append(d)
                print(str(d))
                print('--------')

        return {
            'content':str(comments),
            'type':'comment',
            'method':'database'
        }

    def comment_list_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')        
        lists = soup('div', 'comment-list')[0].find_all('li')
        comments = []
        for i in lists:
            t = i.find('div', 'J_brief-cont')
            if t is not None:
                d = {}
                d['overview'] = ''
                d['params1'] = ''
                d['params2'] = ''
                d['params3'] = ''
                d['comment'] = ''
                d['time'] = ''
                v = i.find('div', 'user-info').find_all('span')
                d['overview'] = str(int(v[0]['class'][1].split('star')[1]) / 10)
                index = 1
                for j in v[1:]:
                    if j['class'][0] == "comm-per":
                        print('jump')
                        continue
                    name = 'params' + str(index)
                    index += 1
                    d[name] = j.get_text()
                # like = i.find('div', 'comment-recommend')
                # if like is not None:
                #     like = like.find('a').get_text()
                time = i.find('span', 'time').get_text().split('\xa0\xa0')[0]
                content = t.get_text()
                if len(time.split('-')) < 3:
                    time = str(date.now().year)[2:] + '-' + time
                # d['like'] = like
                d['comment'] = content.strip()
                d['time'] = time
                comments.append(d)
                print(str(d))
                print('--------')

        return {
            'content':str(comments),
            'type':'comment',
            'method':'database'
        }

    def on_result(self, result):
        type_name = {'food':'美食', 'play':'休闲娱乐', 'shopping':'购物', 'hotel':'酒店', 'spot':'景点'}
        if result is not None:
            print(result)
            if result['method'] == 'database':
                if result['type'] == 'comment':
                    content = eval(result['content'])
                    values = []
                    for i in content:
                        date = '20' + i['time']
                        values.append((i['shopNo'], i['comment'], date, i['params1'],
                            i['params2'], i['params3'], i['overview']))
                    print(values)
                    conn = None
                    try:
                        dsn = cx_Oracle.makedsn('localhost', 1521, 'urbandeve')
                        conn = cx_Oracle.connect(user='C##WWPA', password='wwpa5678', dsn=dsn)
                        try:
                            cursor = conn.cursor()
                            cursor.setinputsizes(cx_Oracle.STRING, cx_Oracle.CLOB,
                                cx_Oracle.DATETIME, cx_Oracle.STRING,
                                cx_Oracle.STRING, cx_Oracle.STRING, cx_Oracle.NATIVE_FLOAT)
                            cursor.prepare('''insert into TBL_DPCOMMENTS 
                                (SHOPNO, CONTENT, COMMENTDATE,
                                PARAMETER1, PARAMETER2, PARAMETER3, OVERALL) 
                                values(:1, :2, to_date(:3, 'yyyy-mm-dd'), :4, :5, :6, :7)''')
                            for i in values:
                                cursor.execute(None, i)
                            conn.commit()
                        finally:
                            cursor.close()
                    finally:
                        if conn is not None:
                            conn.close()
                else:
                    types = type_name[result['type']]
                    print(types)
                    content = eval(result['content'])
                    values = (content['address'], content['shopName'],
                        content['avg'], content['commentsNum'], types, content['params1'], content['params2'],
                        content['params3'], self.city_name[content['city']],
                        content['overview'], content['shopNo'])
                    print(values)
                    conn = None
                    try:
                        dsn = cx_Oracle.makedsn('localhost', 1521, 'urbandeve')
                        conn = cx_Oracle.connect(user='C##WWPA', password='wwpa5678', dsn=dsn)
                        try:
                            cursor = conn.cursor()
                            sql = '''update TBL_DPSHOPS set LOCATION = '%s',
                                NAME = '%s', PERSPEND = '%s', SUMCOMMENTS = '%s', TYPE = '%s',
                                PARAMETER1 = '%s', PARAMETER2 = '%s', PARAMETER3 = '%s',
                                ASCRIPTIONCITY = '%s', OVERALL = '%s' where SHOPNO ='%s' '''
                            sql = sql % values
                            print(sql)
                            cursor.prepare(sql)
                            # z = (values[0],)
                            cursor.execute(None)
                            print(cursor.rowcount)
                            if cursor.rowcount == 0:
                                values = (content['shopNo'], content['address'], content['shopName'],
                                    content['avg'], content['commentsNum'], types, content['params1'], content['params2'],
                                    content['params3'], self.city_name[content['city']],
                                    content['overview'])
                                cursor.prepare('''insert into TBL_DPSHOPS 
                                (SHOPNO, LOCATION, NAME,
                                PERSPEND, SUMCOMMENTS, TYPE, PARAMETER1, PARAMETER2, PARAMETER3,
                                ASCRIPTIONCITY, OVERALL) 
                                values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)''')
                                cursor.execute(None, values)
                            conn.commit()
                        finally:
                            cursor.close()
                    finally:
                        if conn is not None:
                            conn.close()

            else:
                content = eval(result['content'])
                values = []
                for i in content:
                    values.append((i['message'], i['shopNo']))
                if result['type'] == 'hot':
                    update_sql(values, 'TRADINGAREA')
                else:
                    update_sql(values, 'SUBWAYSTATION')

                    

    def update_sql(values, column):
        for i in values:
            conn = None
            try:
                dsn = cx_Oracle.makedsn('localhost', 1521, 'urbandeve')
                conn = cx_Oracle.connect(user='C##WWPA', password='wwpa5678', dsn=dsn)
                try:
                    cursor = conn.cursor()
                    for i in values:
                        sql = '''update TBL_DPSHOPS set %s = '%s' where SHOPNO = '%s' ''' 
                        t = (column,) + i
                        sql = sql % t 
                        cursor.prepare(sql)
                        cursor.execute(None)
                        print(cursor.rowcount)
                        if cursor.rowcount == 0:
                            values = (values[1], values[0])
                            cursor.prepare('''insert into TBL_DPSHOPS 
                            (SHOPNO, %s) 
                            values(:1, :2)''' % column)
                            cursor.execute(None, values)
                        conn.commit()
                finally:
                    cursor.close()
            finally:
                if conn is not None:
                    conn.close() 