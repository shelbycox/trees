import operator

error = 0.00001

def normalize_heights(L, h):
	for t in L:
		tree_height = max([t[k] for k in t.keys()])
		adjust = tree_height - h
		for k in t.keys():
			t[k] = t[k] - adjust
	
	return L

def get_tropical_line(u, v, recMu=False):
	try:
		mu = sorted([u[k] - v[k] for k in u.keys()])

		L = [u]
		if recMu:
			L = [(u, mu[0])]

		for scalar in mu:
			if recMu:
				L.append(({k : max(scalar + v[k], u[k]) for k in u.keys()}, scalar))
			else:
				L.append({k : max(scalar + v[k], u[k]) for k in u.keys()})

		if recMu:
			L.append((v, mu[-1]))
		else:
			L.append(v)

		return L
	
	except KeyError:
		print('Error: u, v must be trees on the same leaves.')

def argmaxm(u):
	global error
	values = sorted(list(set(u.values())))
	##account for rounding errors
	rounded_values = [values[0]]
	for v in values:
		#if the next value differs by more than acceptable error, add it as a new value to the list
		if abs(values[-1] - v) > error:
			rounded_values.append(v)
	return [[k for (k,v) in u.items() if v - rounded_values[-i] < error] for i in range(1,len(rounded_values)+1)]

##should also implement a compare_trees_coarse

def compare_trees(u, v):
	u_arg = argmaxm(u)
	v_arg = argmaxm(v)

	for i in range(len(u_arg)):
		try:
			if u_arg[i] != v_arg[i]:
				return False
		except KeyError:
			return False

	return True

def reduce_line(L):
	line = L.copy()
	i = 0
	while i < len(line) - 1:
		#print(type(line[i]), type(line[i+1]))
		u = None
		v = None
		if type(line[i]) == tuple:
			##get to this case if we are recording other information for each tree in the line
			u = line[i][0]
	
		if type(line[i+1]) == tuple:
			v = line[i+1][0]

		if u == None:
			u = line[i]

		if v == None:
			v = line[i+1]
		
		if compare_trees(u,v):
			##the trees are the same, so remove the first one
				line.pop(i)
				##stay on the same index
				i = i - 1
		i = i + 1

	return line

def get_line_int(u,v):
	##get the reduced tropical line from u to v
	line = reduce_line(get_tropical_line(u,v,True))
	
	mu = [line[0][1]]
	for i in range(1,len(line)):
		mu.append((line[i][1] + line[i-1][1])/2)
		mu.append(line[i][1])
	
	return [{k : max(m + u[k], v[k]) for k in u.keys()} for m in mu]

def left_right_split(leaves, a):
	left = [leaves[0]]
	right = []
	
	i = leaves[0]
	for k in range(1, len(leaves)):
		j = leaves[k]
		if (i,j) in a:
			right.append(j)
		else:
			left.append(j)
	
	return left, right, len(right) == 0

def tree_rest(u, leaves):
	return {(i, j) : u[(i,j)] for (i,j) in u.keys() if i in leaves and j in leaves}

def rec_tree_paren(u, leaves):
	##if there's just two leaves left, they're as close as they can get
	if len(set(leaves)) < 3:
		return leaves
	
	##split at the highest branches of the current (sub)tree
	#print(argmaxm(u), leaves)
	branches = split(leaves, argmaxm(u)[0])
	print(argmaxm(u)[0])
	
	##regard each branch as its own tree
	rests = [tree_rest(u, b) for b in branches]
	
	return [rec_tree_paren(rests[i], branches[i]) for i in range(len(branches))]

def split(leaves, a):
	done = False
	splits = []
	while done == False:
		##left = leftmost branch, right = everything else,
		##done = True only if right is itself a branch
		left, right, done = left_right_split(leaves, a)
		print(left, right, done)
		
		##add the leftmost branch to the list of splits
		splits.append(left)
		
		##then try to split the right again
		leaves = right
		
	return splits

def print_path(u,v):
	line = reduce_line(get_tropical_line(u,v))
	for T in line:
		print(rec_tree_paren(T, list(set([i for (i,j) in T.keys()]))))

def get_fine_codim(u):
	l = len(argmaxm(u))
	n_leaves = max([i for (i,j) in u.keys()])
	return n_leaves - 1 - l

def get_coarse_codim(u):
	a = argmaxm(u)
	fine_ties = 0
	for t in a:
		if not all_pairs(t):
			fine_ties = fine_ties + 1
	
	return get_fine_codim(u) - fine_ties

def all_pairs(L):
	elts = list(set([i for (i,j) in L]))
	
	for i in range(len(elts)):
		for j in range(i+1, len(elts)):
			if (i,j) not in L:
				return False
	
	return True

def get_heights(u):
	return sorted(set([h for h in u.values()]))