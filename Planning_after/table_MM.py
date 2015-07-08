#!/usr/bin/env python3
'''茂名规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = '''http://csgh.maoming.gov.cn/certselarea.aspx?id=411016'''
html = urlopen(url).read()
# print(html)
soup = BeautifulSoup(html, 'html.parser')
td = soup.find_all('table')[5].find_all('td')
tabs = []
for i in range(len(td)):
	temp = td[i].get_text()
	if len(temp) != 0:
		tabs.append(td[i].get_text())
	else:
		tabs.append(None)
result = {}
for i in range(0, len(tabs), 2):
    result[tabs[i]] = tabs[i + 1]
print(result)