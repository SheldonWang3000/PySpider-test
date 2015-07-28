import redis
from bs4 import BeautifulSoup
import mysql.connector

def update_flag(rowid):
	command = '''update tbl_OrglPblc set StructuredState = 1 where pk_OrglPblc = %s'''
	command = command % rowid
	cursor.execute(command)
	conn.commit()

def FS(path, rowid, type_name):
	html = ''
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	th = soup.find_all('th')[1:10]
	td = soup.find_all('td')[:-1]
	result = {}
	for i in range(len(th)):
		result[th[i].string] = td[i].string
	print(result)
	update_flag(rowid)
def HY(path, rowid, type_name):
	html = ''
	with open(path, 'r') as f:
		html = f.read()
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
	update_flag(rowid)

def QY(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	td = soup.find_all('td')[1:]
	tabs = []
	for i in td:
		tabs.append(i.string) 
	result = {}
	for i in range(0, len(tabs), 2):
	    result[tabs[i]] = tabs[i + 1]
	print(result)
	update_flag(rowid)

def ST(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	td = soup.find_all('table')[0].find_all('td')
	tabs = []
	for i in range(len(td)):
		tabs.append(td[i].get_text().strip('\n').strip('\xa0').strip('\xa0 \xa0'))
	result = {}
	for i in range(0, len(tabs), 2):
	    result[tabs[i]] = tabs[i + 1]
	print(result)
	update_flag(rowid)

def ZQ(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	left = soup.find_all('div', 'lefts')
	left = left[0].find_all('div')
	right = soup.find_all('div', 'right')
	right = right[0].find_all('div')
	right = right[1:]
	right = right[:4] + right[5:]
	names = ['编号', '核发机关', '日期', '建设项目名称', '建设单位名称', '建设项目依据', '建设项目拟选位置',
		'拟用地面积', '拟建设规模', '附图及附件名称']
	tabs = []
	result = {}
	for i in left:
		tabs.append(i.get_text())
	for i in right:
		tabs.append(i.get_text().strip('\n').strip('\r\n').strip())
	for i in range(len(names)):
		result[names[i]] = tabs[i]
	print(result)
	update_flag(rowid)

def ZS(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	td = soup.find_all('td')
	names = []
	for i in td[1:8]:
		names.append(i.get_text().strip('\n'))
	result_set = []
	for i in range(int((len(td) - 8) / 7)):
		result = {}
		for j in range(7):
			result[names[j]] = td[8 + 7 * i + j].get_text().strip('\n')
		result_set.append(result)
	print(result_set)
	update_flag(rowid)

def MM(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
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
	update_flag(rowid)

def GZ_after(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find_all('table')
	table = table[6]
	td = table.find_all('td')
	tabs = []
	for i in range(len(td)):
	    temp = td[i].string.strip()
	    if len(temp) != 0:
	        tabs.append(td[i].string.strip())
	result = {}
	for i in range(0, len(tabs), 2):
	    result[tabs[i]] = tabs[i + 1]
	print(result)
	update_flag(rowid)

def FS(path, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	th = soup.find_all('th')[1:10]
	td = soup.find_all('td')[:-1]
	result = {}
	for i in range(len(th)):
		result[th[i].string] = td[i].string
	print(result)
	update_flag(rowid)

def DG(paht, rowid, type_name):
	html = ''	
	with open(path, 'r') as f:
		html = f.read()
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
	update_flag(rowid)

def CZ(path, rowid, type_name):
	html = ''
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	tr = soup.find_all('tr')
	td = tr[4].find_all('td')
	names = []
	for i in td:
		names.append(i.get_text())
	result_set = []
	tr = tr[5:len(tr) - 3]
	for i in tr:
		td = i.find_all('td')
		result = {}
		tabs = []
		for j in td:
			tabs.append(j.get_text())
		for k in range(len(names)):
			result[names[k]] = tabs[k]
		result_set.append(result)
	print(result_set)
	update_flag(rowid)

def GZ(path, rowid, type_name):
	html = ''
	with open(path, 'r') as f:
		html = f.read()
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find_all('table')
	table = table[4]
	td = table.find_all('td')
	tabs = []
	for i in range(len(td)):
		tabs.append(td[i].string)
	# print(tabs)
	result = {}
	for i in range(0, len(tabs), 2):
		result[tabs[i]] = tabs[i + 1]
	# print(result)
	update_flag(rowid)

if __name__ == '__main__':
	r = redis.Redis()
	key = 'analysis'
	conn = mysql.connector.connect(user='root', password='254478_a', database='mydb')
	cursor = conn.cursor(dictionary=True)
	city_def = {'GZ':GZ, 'CZ':CZ, 'DG':DG, 'GZ_after':GZ_after, 'MM':MM,
				'QY':QY, 'ST':ST, 'ZQ':ZQ, 'ZS':ZS, 'HY':HY}

	type_table = {'选址意见书':'tbl_OpinOfPrjLoc', '建设用地规划许可证':'tbl_LicOfConstLand',
					'建设工程规划许可证':'tbl_PlanLicOfConstLand', '规划验收合格证':'tbl_CertForPlanOfConstPrj',
					'工程规划验收合格通知书':'tbl_AnceCertPlanConstPrj', '批前公示':'tbl_PreAppdPblc',
					'批后公布':'tbl_AppdPblc', 'Unknow':'Unknow', '乡村建设规划许可证':''}
	while True:
		s = r.blpop(key, 0)[1]
		print(s)
		d = eval(s)
		path = d['path'] + 'page.html'
		rowid = d['rowid']
		city = d['city']
		type_name = type_table[d['type'].decode('utf-8')]
		if type_name != 'Unknow':
			city_def[city](path, rowid, type_name)
		print('done')
