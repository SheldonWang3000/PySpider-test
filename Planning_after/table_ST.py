#!/usr/bin/env python3
'''汕头规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = '''http://www.stghj.gov.cn/Item/5085.aspx'''
html = urlopen(url).read()
# print(html)
soup = BeautifulSoup(html, 'html.parser')
td = soup.find_all('table')[0].find_all('td')
tabs = []
for i in range(len(td)):
	tabs.append(td[i].get_text().strip('\n').strip('\xa0').strip('\xa0 \xa0'))
result = {}
for i in range(0, len(tabs), 2):
    result[tabs[i]] = tabs[i + 1]
print(result)