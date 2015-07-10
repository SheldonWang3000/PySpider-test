from cStringIO import StringIO
from PIL import Image
import urllib2
import os
# url = 'http://dcs.conac.cn/image/red.png'
url = 'http://121.10.6.230/dggsweb/Disp.aspx?id=5127'
i = Image.open(StringIO(urllib2.urlopen(url).read()))
print i.size
width, height = i.size
if width >= 40 and height >= 40:
	filename = os.path.basename(url)
	print filename
	print i.format
	try:
		i.save('/root/' + filename)
	except KeyError:
		import md5
		m = md5.new()
		m.update(filename)
		i.save('D:/' + m.hexdigest() + '.' + i.format)