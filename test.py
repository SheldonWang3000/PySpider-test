from bs4 import BeautifulSoup
import xmltodict
import re
from html.parser import HTMLParser
with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
	html = f.read()
soup = BeautifulSoup(html, 'html.parser')
t = soup('iframe')[0]['src'].split('?')[-1].split('&')
k = {}
for i in t:
	temp = i.split('=')
	k[temp[0]] = temp[1]
print(k['uf'])