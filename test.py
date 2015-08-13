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
t = soup('a', 'last-page')
# t = len(t)
# for i in t:
	# print(i['href'])
print(t)
# for i in t:
	# print(i)