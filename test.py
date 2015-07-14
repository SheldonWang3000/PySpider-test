from bs4 import BeautifulSoup
from html.parser import HTMLParser
with open('/home/teer/2.html', 'r') as f:
	html = f.read()
soup = BeautifulSoup(html, 'html.parser')
t = soup('table', {'id':'bookindex'})[0].find_all('a')
# print(len(t))
for i in t:
	print(i['href'])