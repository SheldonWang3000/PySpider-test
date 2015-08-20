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
t = soup('img', src=True) + soup('img', {'data-src': re.compile(r'')})
# t = len(t)
for i in t:
	try:
		print('src:' + i['src'])
	except:
		print('data-src:' + i['data-src'])
# print(t)
# for i in t:
	# print(i)