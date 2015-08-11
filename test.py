# from bs4 import BeautifulSoup
# import re
# import urllib.parse
# from html.parser import HTMLParser
# from urllib.parse import urljoin
# from pyquery import PyQuery as pq
# import os
# with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
# 	html = f.read()
# soup = BeautifulSoup(html, 'html.parser')
# t = soup('table', 'dh')[0].find_all('a', {'target':'_blank'})
# print(len(t))
# for i in t:
	# print(i)

import urllib.request
# import time
# time.sleep(0.001)
url = 'http://www.hfjs.gd.gov.cn/csshome/style.css'
# urllib.request.urlopen(url)
urllib.request.urlretrieve(url, '/home/sheldon/a.css')
