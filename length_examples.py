import prufer as pf
import tropicalLines as tl

def test_1():
	for j in range(10):
		l0 = ((10+j-1)*(10+j-2))/2
		print(10+j, l0)
		for i in range(10):
			u, v = pf.rand_pair(10+j)
			print(u)
			line = tl.get_tropical_line(u,v)
			red_line = tl.reduce_line(line)
			l1 = len(line)
			l2 = len(red_line)
			print(l1, l2, l2 - l1, l2/l0)

		##most lines are 30-40% of the maximum length
		##and this still includes internal ties!
		##how do I compare without caring about internal ties?
		##also need to add the number of 4 stars to the length
		##so need a method that gets the codimension of the line

test_1()