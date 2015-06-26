from cStringIO import StringIO
from PIL import Image
import urllib2
url = 'http://dcs.conac.cn/image/red.png'
i = Image.open(StringIO(urllib2.urlopen(url).read()))
print i.size