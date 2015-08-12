import re
import hashlib
import redis
import http
import urllib.request
from urllib.parse import unquote
from PIL import Image
from io import BytesIO
import time
from functools import wraps


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

@retry(urllib.request.URLError, tries=4)
def open_url(opener, url):
	return opener.open(url)

@retry(urllib.request.URLError, tries=4)
def download_url(url, path):
	urllib.request.urlretrieve(url, path)

def download_attachment(url, path):
	try:
		opener = urllib.request.build_opener()
		headers= {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
		}
		opener.addheaders = headers.items()
		urllib.request.install_opener(opener)
		download_url(url, path)
	except urllib.request.HTTPError:
		print('404')

def download_image(url, path):
	# height = 400
	# width = 400
	height = 0
	width = 0
	try:
		opener = urllib.request.build_opener()
		headers= {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
		}
		opener.addheaders = headers.items()
		f = open_url(opener, url)
		if height * width == 0:
			with open(path, 'wb') as code:
				code.write(f.read())
		else:
			i = Image.open(BytesIO(f.read()))
			temp_width, temp_height = i.size
			if temp_width >= width and temp_height >= height:
				i.save(path)
	except urllib.request.HTTPError:
		print('404')

if __name__ == '__main__':
	r = redis.Redis()
	key = 'download'
	while True:
		try:
			s = r.blpop(key, 0)[1]
			print(s)
			d = eval(s)
			path = d['path'] + d['file_name']
			url = d['url']
			link_type = d['type']
			if link_type == 'image':
				download_image(url, path)
			else:
				download_attachment(url, path)
			print('done')
		except Exception as e:
			break
