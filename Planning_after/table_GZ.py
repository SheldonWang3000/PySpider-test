#!/usr/bin/env python3
'''广州规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen('http://www.upo.gov.cn/gs/Content.aspx?cid=29301').read().decode('utf-8', 'ignore')
soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
table = soup.find_all('table')
table = table[6]
td = table.find_all('td')
tabs = []
for i in range(len(td)):
    temp = td[i].string.strip()
    if len(temp) != 0:
        tabs.append(td[i].string.strip())
result = {}
for i in range(0, len(tabs), 2):
    result[tabs[i]] = tabs[i + 1]
print(result)
