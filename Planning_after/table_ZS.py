#!/usr/bin/env python3
'''中山规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen('http://www.zsghj.gov.cn/shtml/p-95237-1.html').read()
soup = BeautifulSoup(html, 'html.parser')
td = soup.find_all('td')
names = []
for i in td[1:8]:
	names.append(i.get_text().strip('\n'))
result_set = []
for i in range(int((len(td) - 8) / 7)):
	result = {}
	for j in range(7):
		result[names[j]] = td[8 + 7 * i + j].get_text().strip('\n')
	result_set.append(result)
print(result_set)