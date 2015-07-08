#!/usr/bin/env python3
'''肇庆规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = '''http://www.zqplan.gov.cn/ghxk-49193-1.aspx'''
html = urlopen(url).read()
# print(html)
soup = BeautifulSoup(html, 'html.parser')
left = soup.find_all('div', 'lefts')
left = left[0].find_all('div')
right = soup.find_all('div', 'right')
right = right[0].find_all('div')
right = right[1:]
right = right[:4] + right[5:]
names = ['编号', '核发机关', '日期', '建设项目名称', '建设单位名称', '建设项目依据', '建设项目拟选位置',
	'拟用地面积', '拟建设规模', '附图及附件名称']
tabs = []
result = {}
for i in left:
	tabs.append(i.get_text())
for i in right:
	tabs.append(i.get_text().strip('\n').strip('\r\n').strip())
for i in range(len(names)):
	result[names[i]] = tabs[i]
print(result)