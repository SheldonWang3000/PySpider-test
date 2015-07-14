import urllib.parse
from html.parser import HTMLParser
# s = 'http://121.10.6.230/dggsweb/PHGSFJ/PHjsxmxzFJ.aspx?%cf%ee%c4%bf%ca%dc%c0%ed%b1%e0%ba%c5=%cb%c9%c9%bd%ba%fe2014000109&%b9%ab%ca%be=%c5%fa%ba%f3%b9%ab%ca%be'
# s = 'http://121.10.6.230/dggsweb/Transfer.aspx?xmslbh=%CB%C9%C9%BD%BA%FE2014000109&gs=%C5%FA%BA%F3%B9%AB%CA%BE&ywlx=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9'
# s = 'http://121.10.6.230/dggsweb/Transfer.aspx?xmslbh=%CB%C9%C9%BD%BA%FE2014000109gs=%C5%FA%BA%F3%B9%AB%CA%BEywlx=%BD%A8%C9%E8%CF%EE%C4%BF%D1%A1%D6%B7%D2%E2%BC%FB%CA%E9'
# k = '%CB%C9%C9%BD%BA%FE2014000109'
t = 'Transfer.aspx?xmslbh=松山湖2014000109&amp;gs=批后公示&amp;ywlx=建设项目选址意见书'
h = HTMLParser()
t = h.unescape(t)
l = t.split('?')
a = l[1].split('&')
print(a)
link = ''
link += urllib.parse.quote('项目受理编号'.encode('gbk')) + '=' + urllib.parse.quote(a[0].split('=')[1].encode('gbk')) + '&' + urllib.parse.quote('公示'.encode('gbk')) + '=' + urllib.parse.quote(a[1].split('=')[1].encode('gbk'))
for i in a:
	temp = i.split('=')
	print(temp)
	# link = link + temp[0] + '=' + urllib.parse.quote(temp[1].encode('gbk')) + '&'
print(link)
domain = 'http://121.10.6.230/dggsweb/PHGSFJ/PHjsxmxzFJ.aspx?'
print(domain + link)
