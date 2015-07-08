#!/usr/bin/env python3
'''潮州规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = '''http://czcsgh.gov.cn/jsyd_s.asp'''
html = urlopen(url).read()
# print(html)
soup = BeautifulSoup(html, 'html.parser')
tr = soup.find_all('tr')
td = tr[4].find_all('td')
names = []
for i in td:
	names.append(i.get_text())
print(names)
result_set = []
tr = tr[5:len(tr) - 3]
for i in tr:
	td = i.find_all('td')
	result = {}
	tabs = []
	for j in td:
		tabs.append(j.get_text())
	for k in range(len(names)):
		result[names[k]] = tabs[k]
	result_set.append(result)
print(result_set)