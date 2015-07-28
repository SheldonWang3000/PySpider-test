'''河源规划局'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = '''http://www.ghjsj-heyuan.gov.cn/certificate.asp?categoryid=403'''
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
table = soup('table')[8].find_all('td')
tabs = []
for i in table:
	tabs.append(i.find('strong').get_text())
print(tabs)

result_set = []
table = soup('table')[9].find_all('tr')
for i in table:
	temp = i('td')
	if len(temp) != 1:
		d = {}
		for j in range(len(tabs)):
			d[tabs[j]] = temp[j].get_text()
		result_set.append(d)
for i in result_set:
	print(i)