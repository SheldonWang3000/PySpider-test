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
# t = soup('a', {'onclick': re.compile(r'titlelinks')})
# print(len(t))
# for i in t:
# 	temp = i['onclick']
# 	left = temp.find('(')
# 	right = temp.rfind(')')
# 	temp = temp[left + 1:right]
# 	temp = temp.split(',')
# 	if temp[3] == '2':
# 		print('2')
# 	elif temp[3] == '1':
# 		print('1')
import urllib.request
import time
time.sleep(0.001)
url = 'http://www.hfjs.gd.gov.cn/csshome/style.css'
urllib.request.urlretrieve(url, '/home/sheldon/a.css')
