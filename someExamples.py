import prufer as pf
import tropicalLines as tl

def tree_to_dict(u, n):
	##given a vector, get a dict
	u_dict = dict()
	i = 1
	j = 2
	for dex in u:
		u_dict[(i,j)] = dex
		u_dict[(j,i)] = dex
		if j < n:
			j = j + 1
		else:
			i = i + 1
			j = i + 1

	return u_dict

def test_1():
	for i in range(100):
		u = pf.gen_tree(5)
		m = pf.get_metric(u)
		T = {(i, j) : m[(i,j)] for (i,j) in m.keys() if i*j != 0}
		for k in T.keys():
			if T[k] <= 0:
				print(k, T[k])

def test_2():
	print('running test 2')
	for i in range(100):
		u = pf.gen_tree(5)
		m = pf.get_metric(u)
		T = {(i, j) : m[(i,j)] for (i,j) in m.keys() if i*j != 0}

		v = pf.gen_tree(5)
		n = pf.get_metric(v)
		R = {(i, j) : n[(i,j)] for (i,j) in m.keys() if i*j != 0}

		line = tl.get_tropical_line(T,R,True)
		mus = [line[i][1] for i in range(len(line))]
		print(mus)

def test_3():
	print('running test 3')
	u = {(1, 2): 0.0, (2, 1): 0.0, (1, 3): 2.0, (3, 1): 2.0, (1, 4): 2.0, (4, 1): 2.0, (2, 3): 2.0, (3, 2): 2.0, (2, 4): 2.0, (4, 2): 2.0, (3, 4): -2.0, (4, 3): -2.0}
	v = {(1, 2): 0.0, (2, 1): 0.0, (1, 3): 2.0, (3, 1): 2.0, (1, 4): 0.0, (4, 1): 0.0, (2, 3): 2.0, (3, 2): 2.0, (2, 4): -2.0, (4, 2): -2.0, (3, 4): 2.0, (4, 3): 2.0}

	line = tl.get_tropical_line(u,v)

	for t in line:
		print(tl.argmaxm(t))

	print()

	line = tl.reduce_line(line)

	for t in line:
		print(tl.argmaxm(t))

def test_4():
	print('running test 4')
	u = tree_to_dict([8,200,4,8,200,200,8,2,200,200,200,6,8,200,200], 6)
	v = tree_to_dict([2,4,6,6,6,4,6,6,6,6,6,6,3,3,1], 6)

	print(u)
	print(v)

	print(tl.rec_tree_paren(u,[1,2,3,4,5,6]))

	print(tl.argmaxm(v))


	line = tl.normalize_heights(tl.get_line_int(u,v), 2)

	print(line[-1])

	# for T in line:
	# 	print(tl.argmaxm(T))

def test_5():
	print('running test 5')
	u = tree_to_dict([10,200,200,2,10,200,200,200,200,10,6,200,200,12,200,200,4,12,200,200,12,8,10,200,200,200,200,12], 8)
	v = tree_to_dict([2,4,6,8,8,8,8,4,6,8,8,8,8,6,8,8,8,8,8,8,8,8,5,5,5,3,3,1], 8)

	print(v)
	print()

	print(tl.argmaxm(v))

	R = tl.rec_tree_paren(v, [1,2,3,4,5,6,7,8])
	print(R)

def test_6():
	print('running test 6')
	u = tree_to_dict([40,40,40,40,30,30,30,20,20,10], 5)
	v = tree_to_dict([1,2,3,4,2,3,4,3,4,4], 5)

	print(u)
	print(v)

print()
# test_6()
# test_4()

# [[(1, 3), (3, 1), (1, 6), (6, 1), (2, 3), (3, 2), (2, 6), (6, 2), (3, 4), (4, 3), (3, 5), (5, 3), (4, 6), (6, 4), (5, 6), (6, 5)], [(1, 4), (4, 1), (1, 5), (5, 1), (2, 4), (4, 2), (2, 5), (5, 2), (3, 6), (6, 3)], [(4, 5), (5, 4)], [(1, 2), (2, 1)]]

u = tree_to_dict(['a',1,1,1,1,'q'], 4)
v = tree_to_dict(['b','b+c',1,'b+c',1,1], 4)

print(u)
print(v)