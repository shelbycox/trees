import prufer as pf
import numpy as np
import matplotlib.pyplot as plt

def fast_get_descendants(p):
	n = len(p) + 2
	descendants = {k : [] for k in range(n)}
	num_leaves = int((len(p) + 4)/2)
	leaves = [i for i in range(num_leaves)]
	past_leaves = []
	while len(p) > 0:
		##add the descendants for parents of current leaves
		for i in range(num_leaves):
			##k is the vertex we will add descendants to
			k = p[i]
			##add leaves[i] and the descendants of leaves[i] to the descendants of k
			descendants[k] = descendants[k] + [leaves[i]] + descendants[leaves[i]]

		##update the prufer sequence by truncating the first num_leaves indices
		p = p[num_leaves + 1 :]
		##update the past leaves
		past_leaves = past_leaves + leaves
		##new leaves are vertices that were not previously leaves and do not appear in the prufer sequence now
		leaves = [i for i in range(n) if i not in past_leaves and i not in p]
		##update the number of leaves
		num_leaves = len(leaves)

	return descendants

##given two random prufer sequences, want to compute the likelihood that (n+1,n+1) is in the image of phi
##need to ``merge" branches
def fast_get_branches(p,target):
	num_leaves = int((len(p) + 4)/2)
	branches = [[i] for i in range(num_leaves)]
	leaves = [i for i in range(num_leaves)]
	past_leaves = []
	while len(p > 0):
		new_branches = [b + [p[leaves.index(i)] for i in b if i in leaves] for b in branches]
		

	##at the end, remove internal vertices that were added

def get_branches(p,target):
	adj = pf.build_tree(p)
	# print(adj)

	##get the three internal vertices adjacent to the target vertex
	branches = [i for i in range(len(adj)) if adj[target][i] != 0]
	# print(branches)

	for b in branches:
		adj[b][target] = adj[target][b] = 0

	##get the descendants of each of those three internal vertices
	##and remove any non-leaf vertices
	return [[d for d in list(set(get_descendants(adj, b))) if d < int((len(p) + 4)/2)] for b in branches]

##given an adjacency matrix, recursively find the descendants of v
def get_descendants(adj,v):
	##if v is a leaf
	if np.count_nonzero(adj[v]) == 0:
		return [v]

	##otherwise, v has children
	children = [i for i in range(len(adj)) if adj[v][i] != 0]

	v_descendants = children
	for c in children:
		##remove the edges between v and its children
		adj[v][c] = adj[c][v] = 0
		##add the descendants of child c to the descendants of v
		v_descendants = v_descendants + get_descendants(adj,c)

	return v_descendants

##returns true if (target,target) is a possible turning point in the tropical line
def t_in_img(p,r,target):
	p_branches = get_branches(p, target)
	r_branches = get_branches(r, target)

	p_root = -1
	r_root = -1
	for b in range(3):
		if 0 in p_branches[b]:
			p_root = b
			break
	for b in range(3):
		if 0 in r_branches[b]:
			r_root = b
			break

	a, b = [i for i in range(3) if i != p_root]
	x, y = [j for j in range(3) if j != r_root]

	ax = set(p_branches[a]) & set(r_branches[x])
	ay = set(p_branches[a]) & set(r_branches[y])
	bx = set(p_branches[b]) & set(r_branches[x])
	by = set(p_branches[b]) & set(r_branches[y])

	return (len(ax) > 0 and len(by) > 0) or (len(ay) > 0 and len(bx) > 0)

# print(t_in_img([5,5,6,7,7,6], [5,6,6,7,7,5], 6))

N = 10000

data = []

for i in range(99,101):
	hits = 0
	for j in range(N):
		p = pf.gen_prufer(i)
		r = pf.gen_prufer(i)
		if t_in_img(p,r,i+1):
			hits = hits + 1
	print(i, hits/N)
	data.append((i, hits/N))

with open('my_data.txt', 'a') as the_file:
	the_file.write(str(data))