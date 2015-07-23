# coding:utf-8
import pysolr

solr_url = "http://localhost:8085/myfullretrieve/"

solr = pysolr.Solr(solr_url, timeout=10)
# result = solr.search('广州 东莞')
# for i in result:
# 	print(i['content'])
# print('-------------')
result = solr.search(['广州 and 冰雹'])
for i in result:
	print(i['content'])

    

