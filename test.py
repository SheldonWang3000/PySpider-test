# import mysql.connector
# conn = mysql.connector.connect(user='root', password='254478_a', database='test')
# cursor = conn.cursor(dictionary=True)
# # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# a = ['1', 'Teer']
# b = ['2', 'Sheldon']
# c = ['6', 'ying']
# c = ['t']
# # cursor.execute('insert into user (id, name) values (%s, %s)', a)
# cursor.execute('insert into cc (name) values (%s)', c)
# print(cursor.lastrowid)
# # conn.commit()
# # cursor.execute('show columns from user;')
# # names = cursor.fetchall()
# # print(names)
# cursor.execute('select * from user;')
# result = cursor.fetchall()
# for i in result:
# 	print(i['name'])
# print(result)
from bs4 import BeautifulSoup
import re
import urllib.parse
from html.parser import HTMLParser
from urllib.parse import urljoin
from pyquery import PyQuery as pq
import os
with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
	html = f.read()
soup = BeautifulSoup(html, 'html.parser')
t = soup('a', {'target':'_blank'})[:-3]
print(len(t))
for i in t:
	print(i['href'])