from pyquery import PyQuery as pq
import os
import urlparse
# a = pq('<img src="../../../../../../../images/gl_ico2.jpg" alt="" class="f_l">')
a = pq('<img src="http://www.laho.gov.cn/images/gl_ico2.jpg" alt="" class="f_l">')
url = 'http://www.laho.gov.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/201506/t20150604_395052.htm'
print a.attr.src
print urlparse.urljoin(url, a.attr.src)