#!/usr/bin/env python3
'''清远规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
url = 'http://120.81.224.155:8084/project/show.php?id=19&typeform=project_site_submission'
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
td = soup.find_all('td')[1:]
tabs = []
for i in td:
	tabs.append(i.string) 
result = {}
for i in range(0, len(tabs), 2):
    result[tabs[i]] = tabs[i + 1]
print(result)