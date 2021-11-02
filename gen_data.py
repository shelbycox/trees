import tropicalLines as tl
import prufer as pf
import math
import matplotlib.pyplot as plt

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

def get_data(u,v,n):
	##get n choose 2, the maximum length of the tropical line
	max_length = int(len(u)/2)

	##get the actual length of lambda as a set
	line = tl.get_tropical_line(u,v)
	actual_lambda_len = len(line)

	##get the actual NNI length
	actual_NNI_len = tl.nni_distance(u,v,n)

	return max_length, round(actual_lambda_len/max_length, 6), round(actual_NNI_len/max_length, 6), actual_NNI_len

def gen_data(N, num_leaves):
	data = []
	for k in range(N):
		T = pf.get_metric(pf.gen_tree(num_leaves+1))
		u = {(i,j) : T[(i,j)] for (i,j) in T.keys() if i != 0 and j != 0}

		R = pf.get_metric(pf.gen_tree(num_leaves+1))
		v = {(i,j) : R[(i,j)] for (i,j) in R.keys() if i != 0 and j != 0}

		data.append(get_data(u,v,num_leaves))

	return data

def avg(N, num_leaves):
	D = gen_data(N, num_leaves)
	nni_lengths = [v[-1] for v in D]
	b = sum([l for l in nni_lengths])
	return b/N

def get_lambda_data(u, v, n):
	##get n choose 2, the maximum length of the tropical line
	max_length = int(len(u)/2)

	##get the actual length of lambda as a set
	actual_lambda_len = len(list(set([u[k] - v[k] for k in u.keys()])))

	return max_length, actual_lambda_len, round(actual_lambda_len/max_length, 6)

def gen_lambda_data(N, num_leaves):
	data = []
	for k in range(N):
		T = pf.get_metric(pf.gen_tree(num_leaves+1))
		u = {(i,j) : T[(i,j)] for (i,j) in T.keys() if i != 0 and j != 0}

		R = pf.get_metric(pf.gen_tree(num_leaves+1))
		v = {(i,j) : R[(i,j)] for (i,j) in R.keys() if i != 0 and j != 0}

		data.append(get_lambda_data(u,v,num_leaves))

	return data

N = 100
for n in range(5, 40):
	D = gen_lambda_data(N, n)
	avg = 0
	for d in D:
		avg = avg + d[1]
	avg = avg/N
	print(n, avg/D[0][0])

# guess = 20*math.log(20)
# D = gen_data(100,20)
# print(D)
# avg = sum([v[1] for v in D])/len(D)
# print(avg)

# fig, ax = plt.subplots()  # Create a figure containing a single axes.
# ax.plot([i for i in range(4, 20)], [avg(100, i) for i in range(4,20)])  # Plot some data on the axes.
# ax.plot([i for i in range(4, 20)], [i*math.log(i) for i in range(4,20)])
# plt.show()

# for i in range(4, 20):
# 	a = avg(100, i)
# 	guess = i*math.log2(i)
# 	print(i, a, guess, a/guess)

##then print averages and stuff, compare to n^2, n log n, n