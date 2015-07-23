# import mysql.connector
# conn = mysql.connector.connect(user='root', password='254478_a', database='test')
# cursor = conn.cursor(dictionary=True)
# # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# a = ['1', 'Teer']
# b = ['2', 'Sheldon']
# # cursor.execute('insert into user (id, name) values (%s, %s)', a)
# # cursor.execute('insert into user (id, name) values (%s, %s)', b)
# # conn.commit()
# # cursor.execute('show columns from user;')
# # names = cursor.fetchall()
# # print(names)
# cursor.execute('select * from user;')
# result = cursor.fetchall()
# for i in result:
# 	print(i['name'])
# # print(result)
# from bs4 import BeautifulSoup
# import re
# import urllib.parse
# from html.parser import HTMLParser
# from urllib.parse import urljoin
# from pyquery import PyQuery as pq
# import os
# with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
# 	html = f.read()
# # p = pq(html)
# # t = p('table[summary="forum_76"]').find('a[class="s xst"]')
# # print(len(t))
# # for i in t.items():
# # 	print(i.attr.href)
# soup = BeautifulSoup(html, 'html.parser')
# t = soup('a', {'class':'nxt'})
# print(len(t))
# for i in t:
# 	print(i['href'])
class A(object):
	def foo(self):
		print('A')

class B(A):
	def foo(self):
		pass
		# super(B, self).foo()
		# print('B')

class C(B):
	def foo(self):
		# super(C, self).foo()
		print('C')

if __name__ == '__main__':
	a = C()
	a.foo()