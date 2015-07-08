import urllib
import urllib2
from httplib import HTTPConnection
url = 'http://www.fsgh.gov.cn/GTGHService/home/SearchData'
params = {'strWhere' : '%2C%2C%2C', 'action': 'xzyjs', 'area': '', 'pageIndex': '1', 'pageSize': '15'}
data = urllib.urlencode(params)
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
html = response.read()
print html