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
t = soup('table', {'id':'ctl00_ContentPlaceHolder1_AxGridView1'})[0].find_all('a', {'target':'_blank'})
t = len(t)
# for i in t:
	# print(i.get_text())
print(t)
# for i in t:
	# print(i)