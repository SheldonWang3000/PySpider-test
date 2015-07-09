# coding=gbk
import threading
import time
def te(num):
	time.sleep(0.5)
	print 'te'
if __name__ == '__main__':
	threads = []
	for i in range(10):
		t = threading.Thread(target=te, args=([100]))
		t.setDaemon(False)
		threads.append(t)
	for i in range(10):
		threads[i].start()
	print 'tttt'
	# time.sleep(1)
# from itertools import repeat
# def testt(a):
# 	print a
# def test((a, b)):
# 	print str(a) + '+' + str(b) + '=' + str(a + b)
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes=6)
#     l = [1, 2, 3]
#     ll = 100
#     # map(test, l, ll)
#     pool.map(test, zip(l, repeat(ll)))
#     pool.close()
#     pool.join()
