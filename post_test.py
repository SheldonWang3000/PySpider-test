import urllib
import urllib2
import re
from bs4 import BeautifulSoup
f = open('/home/teer/1.html', 'r')
html = f.read()
f.close()
soup = BeautifulSoup(html, 'html.parser')
print soup.find(id=re.compile(r'LabelPageCount')).get_text()
# url = 'http://www.fsgh.gov.cn/GTGHService/home/SearchData'
# params = {'strWhere' : '%2C%2C%2C', 'action': 'xzyjs', 'area': '', 'pageIndex': '1', 'pageSize': '15'}
# data = urllib.urlencode(params)
# request = urllib2.Request(url, data)
# response = urllib2.urlopen(request)
# html = response.read()
# print html