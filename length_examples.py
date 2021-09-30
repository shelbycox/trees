import prufer as pf
import tropicalLines as tl

def test_1():
	for j in range(10):
		print(10+j, ((10+j)*(10+j-1))/2)
		for i in range(10):
			u, v = pf.rand_pair(10+j)
			line = tl.get_tropical_line(u,v)
			red_line = tl.reduce_line(line)
			l1 = len(line)
			l2 = len(red_line)
			print(l1, l2, l2 - l1)

test_1()