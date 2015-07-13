import os
import md5
d = '/home/teer/web'
names = os.listdir(d)
print len(names)
d = '/home/teer/web1'
names_old = os.listdir(d)
for i in names_old:
	if i not in names:
		print i