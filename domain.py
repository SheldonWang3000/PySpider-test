import re
url = 'http://zsghj.gov.cn/shtml/p-94590-1.html'
url = url.split('/')[2]
print(url)
url_domain = 'zsghj.gov.cn'
if re.search(url_domain, url):
	print('ok')