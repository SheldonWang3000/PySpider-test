import multiprocessing 
from itertools import repeat
def testt(a):
	print a
def test((a, b)):
	print str(a) + '+' + str(b) + '=' + str(a + b)
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=6)
    l = [1, 2, 3]
    ll = 100
    # map(test, l, ll)
    pool.map(test, zip(l, repeat(ll)))
    pool.close()
    pool.join()