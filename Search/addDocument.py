# coding:utf-8
import pysolr
solr = pysolr.Solr('http://localhost:8085/myfullretrieve/', timeout=10)

document1 = {"docfullid":"1", "content":"广州今天下大雨"}
document2 = {"docfullid":"2", "content":"东莞昨天下冰雹"}
document3 = {"docfullid":"3", "content":"广州明天下冰雹"}
document4 = {"docfullid":"4", "content":"东莞今天晴天"}
document5 = {"docfullid":"5", "content":"潮州是个好地方"}

document_list = []
document_list.append(document1)
document_list.append(document2)
document_list.append(document3)
document_list.append(document4)
document_list.append(document5)
solr.add(document_list)