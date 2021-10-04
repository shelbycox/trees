import prufer as pf
import tropicalLines as tl

def test_1():
	for j in range(10):
		l0 = ((10+j)*(10+j-1))/2
		print(10+j, l0)
		for i in range(10):
			u, v = pf.rand_pair(10+j)
			line = tl.get_tropical_line(u,v)
			red_line = tl.reduce_line(line)
			l1 = len(line)
			l2 = len(red_line)
			print(l1, l2, l2 - l1, l2/l0)

def list_finder(L, i):
	indices = [[j] for j in range(len(L))]
	count = 0
	while count < 100:
		# print(i)
		count = count + 1
		# print(indices)
		new_indices = []
		for I in indices:
			curr = L
			for j in I:
				curr = curr[j]
				# print(curr)
			if type(curr) is int:
				# print('true')
				if curr == i:
					# print(i, curr, 'true true')
					return I
			else:
				for k in range(len(curr)):
					new_I = I.copy()
					new_I.append(k)
					new_indices.append(new_I)
		indices = new_indices

print(list_finder([[1,2],[3,4]], 1))
print(list_finder([[1,2],[3,4]], 2))
print(list_finder([[1,2],[3,4]], 3))
print(list_finder([[1,2],[3,4]], 4))