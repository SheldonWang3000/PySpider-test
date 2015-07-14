import os
import hashlib
import redis
import urllib.request
'''on CentOS'''
from PIL import Image
'''on Ubuntu'''
# import Image
from io import BytesIO
def download_attachment(url, path):
	try:
		attachment_path = path + os.path.basename(url)
		f = urllib.request.urlopen(url)
		with open(attachment_path, 'wb') as code:
			code.write(f.read())
	except urllib.request.HTTPError:
		print('404')

def download_image(url, path):
	height = 300
	width = 300
	try:
		f = urllib.request.urlopen(url)
		if height * width == 0:
			image_path = path + os.path.basename(url)
			with open(image_path, 'wb') as code:
				code.write(f.read())
		else:
			i = Image.open(BytesIO(f.read()))
			temp_width, temp_height = i.size
			if temp_width >= width and temp_height >= height:
				image_path = path + os.path.basename(url)
				try:
					i.save(image_path)
				except KeyError:
					m = hashlib.md5()
					m.update(os.path.basename(url).encode())
					i.save(path + m.hexdigest() + '.' + i.format)
	except urllib.request.HTTPError:
		print('404')

if __name__ == '__main__':
	r = redis.Redis()
	key = 'download'
	while True:
		s = r.blpop(key, 0)[1]
		print(s)
		d = eval(s)
		path = d['path']
		url = d['url']
		link_type = d['type']
		if link_type == 'image':
			download_image(url, path)
		else:
			download_attachment(url, path)
		print('done')
