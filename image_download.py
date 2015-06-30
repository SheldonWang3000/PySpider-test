from cStringIO import StringIO
from PIL import Image
import urllib2
import os
url = 'http://dcs.conac.cn/image/red.png'
i = Image.open(StringIO(urllib2.urlopen(url).read()))
print i.size
width, height = i.size
if width >= 40 and height >= 40:
	filename = os.path.basename(url)
	i.save('D:/' + filename)