from bs4 import BeautifulSoup
import xmltodict
import re
import urllib.parse
from html.parser import HTMLParser
from urllib.parse import urljoin
import os
# with open('/home/sheldon/PySpider-test/test.html', 'r') as f:
# 	html = f.read()
# soup = BeautifulSoup(html, 'html.parser')
# t = soup('table')[2].find_all('a')[0]['href']
# print(t)
def real_path(path):
	arr = urllib.parse.urlparse(path)
	real_path = os.path.normpath(arr[2])
	return urllib.parse.urlunparse((arr.scheme, arr.netloc, real_path, arr.params, arr.query, arr.fragment))
url = 'http://www.zhzgj.gov.cn/WxContent.aspx?WstName=%d2%b5%ce%f1%b9%ab%ca%be&MdlName=%bd%a8%d6%fe%b9%a4%b3%cc%b9%e6%bb%ae%b9%ab%ca%be&ArtId=23254'
a = '/Imgs/anwang.gif'
t = urljoin(url, a)
print(real_path(t))