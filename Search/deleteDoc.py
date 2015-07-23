# coding:utf-8
import pysolr
solr = pysolr.Solr('http://localhost:8085/myfullretrieve/', timeout=10)

solr.delete(q='*')