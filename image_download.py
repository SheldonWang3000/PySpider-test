from cStringIO import StringIO
from PIL import Image
import urllib2
import os
# url = 'http://dcs.conac.cn/image/red.png'
url = 'http://pph.upo.gov.cn/pph/pphImages/2004/08/2004005033.jpg%3E%3C/d'
i = Image.open(StringIO(urllib2.urlopen(url).read()))
print i.size
width, height = i.size
if width >= 40 and height >= 40:
	filename = os.path.basename(url)
	print filename
	i.save('/root/' + filename)