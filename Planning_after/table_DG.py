#!/usr/bin/env python3
'''东莞规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = '''http://121.10.6.230/dggsweb/PHGSFJ/PHjsxmxzFJ.aspx?%cf%ee%c4%bf%ca%dc%c0%ed%b1%e0%ba%c5=%cb%c9%c9%bd%ba%fe2014000109&%b9%ab%ca%be=%c5%fa%ba%f3%b9%ab%ca%be'''
html = urlopen(url).read()
# print(html)
soup = BeautifulSoup(html, 'html.parser')
td = soup.find_all('table', id='DetailsView1')[0].find_all('td')
tabs = []
for i in range(len(td)):
    temp = td[i].string.strip()
    if len(temp) != 0:
        tabs.append(td[i].string.strip())
tabs = tabs[1:]
result = {}
for i in range(0, len(tabs), 2):
    result[tabs[i]] = tabs[i + 1]
print(result)