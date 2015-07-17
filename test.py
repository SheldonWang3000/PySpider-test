from bs4 import BeautifulSoup
import xmltodict
import re
import urllib.parse
from html.parser import HTMLParser
from urllib.parse import urljoin
import os
with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
	html = f.read()
soup = BeautifulSoup(html, 'html.parser')
t = soup('a', {'href': re.compile(r'spcs.asp')})[-1]['href'].split('?')[-1].split('&')
params = {}
for i in t:
	temp = i.split('=')
	params[temp[0]] = temp[1]
print(params)
