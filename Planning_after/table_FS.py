#!/usr/bin/env python3
'''佛山规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
url = 'http://www.fsgh.gov.cn/GTGHService/ViewCase/jsxmghxzyjs/BM00323315'
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
th = soup.find_all('th')[1:10]
td = soup.find_all('td')[:-1]
result = {}
for i in range(len(th)):
	result[th[i].string] = td[i].string
print(result)