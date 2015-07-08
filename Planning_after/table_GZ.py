#!/usr/bin/env python3
'''广州规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen('http://www.upo.gov.cn/channel/szskgk/jsxmxzyjsZ.aspx?caseid=20150500005227').read()
# print(html)
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all('table')
table = table[4]
td = table.find_all('td')
tabs = []
for i in range(len(td)):
	tabs.append(td[i].string)
# print(tabs)
result = {}
for i in range(0, len(tabs), 2):
    result[tabs[i]] = tabs[i + 1]
print(result)
