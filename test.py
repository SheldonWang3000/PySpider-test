# import mysql.connector
# conn = mysql.connector.connect(user='root', password='254478_a', database='test')
# cursor = conn.cursor(dictionary=True)
# # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# a = ['1', 'Teer']
# b = ['2', 'Sheldon']
# c = ['6', 'ying']
# c = ['t']
# cursor.execute('''insert into user (id, name) values ('9', %s)''', c)
# # cursor.execute('insert into cc (name) values (%s)', c)
# print(cursor.lastrowid)
# conn.commit()
# # cursor.execute('show columns from user;')
# # names = cursor.fetchall()
# # print(names)
# cursor.execute('select * from user;')
# result = cursor.fetchall()
# for i in result:
# 	print(i['name'])
# print(result)
# from bs4 import BeautifulSoup
# import re
# import urllib.parse
# from html.parser import HTMLParser
# from urllib.parse import urljoin
# from pyquery import PyQuery as pq
# import os
# with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
# 	html = f.read()
# soup = BeautifulSoup(html, 'html.parser')
# t = soup('img')
# print(len(t))
# for i in t:
# 	print(i['src'])
# def a(t):
# 	print(c)
# 	# print('a' + t)

# if __name__ == '__main__':
# 	d = {'a':a}
# 	c = 'c'
# 	d['a']('b')
# from bs4 import BeautifulSoup
# import re
# with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
# 	html = f.read()
# soup = BeautifulSoup(html, 'html.parser')
# for i in soup('style') + soup('script'):
# 	i.extract()
# content = soup.decode('utf-8')
# content = re.sub(r'<[/!]?\w+[^>]*>', '\n', content)
# content = re.sub(r'<!--[\w\W\r\n]*?-->', '\n', content)
# content = re.sub(r'\s+', '\n', content)
# f = open('con.txt', 'wb')
# f.write(content.encode('utf-8'))
# f.close()
from datetime import datetime, date
print(datetime.now().date())
import mysql.connector
conn = mysql.connector.connect(user='root', password='254478_a', database='mydb')
cursor = conn.cursor(dictionary=True)
values = ['url', 'path', datetime.now().date(), 'city', 'type', 'content']
cursor.execute('''insert into tbl_OrglPblc values ('', %s, %s, B'1', 2, %s, %s, %s, %s)''', values)
conn.commit()