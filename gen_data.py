import tropicalLines as tl
import prufer as pf

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

	return max_length, actual_lambda_len, actual_NNI_len

def gen_data(N, num_leaves):
	for k in range(N):
		T = pf.get_metric(pf.gen_tree(num_leaves+1))
		u = {(i,j) : T[(i,j)] for (i,j) in T.keys() if i != 0 and j != 0}

		R = pf.get_metric(pf.gen_tree(num_leaves+1))
		v = {(i,j) : R[(i,j)] for (i,j) in R.keys() if i != 0 and j != 0}

		print(get_data(u,v,num_leaves))

gen_data(10,5)

##then print averages and stuff, compare to n^2, n log n, n