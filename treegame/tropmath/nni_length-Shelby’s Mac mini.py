from tropicalLines import *
import numpy as np

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

def coarse_comparison(u,v,n):
	##returns true if u,v have the same coarse structure
	##false otherwise

	##idea: prufer sequences will tell me if the trees have the same coarse structure
	##so reconstruct the prufer sequence
	p = get_prufer(u,n)
	q = get_prufer(v,n)
	return p == q

def find_list(L,i):
	indices = [[j] for j in range(len(L))]
	stopper = 100
	while stopper < 100:
		new_indices = []
		for I in indices:
			curr = L
			for j in I:
				curr = curr[j]
			if type(curr) is int:
				if curr == i:
					return I
			else:
				for j in range(len(curr)):
					I_copy = I.copy()
					I_copy.append(j)
					new_indices.append(I_copy)

def List_to_dict(L):
	'''takes a list of lists and returns a dict with keys the (nested) indices of the list'''
	indices = [[i] for i in range(len(L))]
	D = dict()
	stopper = 0
	while stopper < 100:
		if len(indices) == 0:
			break
		new_indices = []
		for I in indices:
			curr = L
			for j in I:
				curr = curr[j]
			#print(curr)
			D[tuple(I)] = curr
			if type(curr) is list:
				for j in range(len(curr)):
					I_copy = I.copy()
					I_copy.append(j)
					new_indices.append(I_copy)
		indices = new_indices
	stopper = stopper + 1
	return D

#print(List_to_dict([[1,2],[[3,4],5]]))

def get_prufer_1(u, num_leaves):
	##compute the number of vertices total
	num_verts = 2*num_leaves - 1

	##get the structure of the tree
	##and convert to dict for easy access
	R = rec_tree_paren(u, [i+1 for i in range(num_leaves)])
	R_dict = List_to_dict(R)

	##start the counter for the current leaf to find
	##and the current parent to assign
	i = 0
	j = num_leaves + 1
	prufer = [-1 for i in range(num_verts)]
	while j <= num_verts:
		i = i + 1
		##if we already assigned an parent to i
		if prufer[i-1] > 0:
			##there's nothing to do
			pass
		##otherwise
		else:
			##get the index of i
			for k in R_dict.keys():
				if R_dict[k] == i:
					I = k

			##check if i should already have a parent
			if len(I) > 1:
				L = R_dict[I[:-1]]
				for e in L:
					if type(e) is int:
						if prufer[e-1] > 0:
							prufer[i] = prufer[e-1]
							break

			##if we haven't set the parent yet
			if prufer[i-1] == -1:

				##set the parent of i
				prufer[i-1] = j


				contains_list = False
				##if R[I] is already an int, we're done
				if type(R_dict[I]) is not int:
					##then set the parents of any other vertices
					##with the same parent as i
					for k in range(R_dict[I]):
						if type(R_dict[I][k]) is int:
							prufer[R_dict[I][k]-1] = j
						else:
							contains_list = True
				
				##if everything in the list containing i has a parent assigned
				if contains_list is False:
					R_dict[I] = j

				j = j + 1
		return prufer


def nni_distance(u,v):
	line = reduce_line(get_tropical_line(u,v))
	count = 0
	for T in line:
		count = count + contribution(T)
	return count

##what about when we stay in codimension 1 or 2 for a while?
##need to properly reduce the line!

def contribution(u):
	C = 2
	R = rec_tree_paren(u)
	indices = [[i] for i in range(len(R))]
	stopper = 0
	if len(indices > C):
		C = len(indices)
	while stopper < 100:
		stopper = stopper + 1
		for I in indices:
			curr = R
			for i in I:
				curr = curr[i]
			if len(curr) > C:
				C = len(curr)

	##if there is a node with three children
	if C == 3:
		##then the tree represents one NNI
		return 1
	##if there is a tree with four children
	if C == 4:
		##then the tree represents two NNIs
		return 2
	##note that generically, there will be exactly one node with more than 2 children, 
	## and it will have at most four children
u = tree_to_dict([1,2,2], 3)
print(rec_tree_paren(u, [i+1 for i in range(3)]))
print(get_prufer(tree_to_dict([1,2,2], 3), 3))

## find deepest number first
## can do this by looking at the length of keys
## assign j as parents of ints in the list R_dict[I[:-1]]
## if everything in the list is an int, then replace the list with j in the dictionary

def all_ints(l):
	for e in l:
		if type(e) is not int:
			return False

	return True

def get_deepest(D):
	I = -1
	M = 0
	for k in D.keys():
		if len(k) > M:
			I = k
			M = len(k)

	return I

def get_prufer_2(u, num_leaves):
	R = rec_tree_paren(u, [i+1 for i in range(num_leaves)])
	R_dict = List_to_dict(R)

	prufer = [-1 for i in range(2*num_leaves - 1)]

	j = num_leaves + 1
	while j <= 2*num_leaves - 1:
		I = get_deepest(R_dict)
		for e in R_dict[I[:-1]]:
			pass


## could I recover the prufer sequence from the metric instead?
## get argmaxm
## name the top vertex j
## save the left and right vertices of j
def get_adj(u, num_leaves):
	A = argmaxm(u)
	num_verts = 2*num_leaves - 1
	j = num_leaves + 1
	children = dict()
	adj = np.zeros((num_verts, num_verts))

	##connect internal vertices
	for a in A:
		ties = get_ties(a)
		print('ties', ties)
		for v in range(len(ties)):
			print(j + v)
			children[j + v] = ties[v]
			for k in range(num_leaves + 1, j)[::1]:
				if set(children[j + v]).issubset(set(children[k])):
					adj[k-1][j-1] = adj[j-1][k-1] = 1
		j = j + v + 1

	##connect leaves
	##loop through leaves
	##go in reverse order through children
	##
	for i in range(num_leaves):
		for k in range(num_leaves + 1, j)[::-1]:
			if i+1 in children[k]:
				adj[k-1][i] = adj[i][k-1] = 1
				break

	return adj

def get_ties(a):
	leaves = list(set([i for (i,j) in a]))
	ties = {j : j for j in leaves}
	for (i,j) in a:
		m = min(ties[i], ties[j])
		ties[i] = ties[j] = m

	return [[i for i in leaves if ties[i] == j] for j in list(set(ties.values()))]

def get_prufer(T):
	P = []
	u = 0
	while u < len(T):
		##if i is a leaf
		if np.count_nonzero(T[u]) == 1:
			##find the vertex adjacent to i
			v = -1
			for i in range(len(T)):
				if T[u][i] != 0:
					v = i
					break

			##add it to the Prufer sequence
			P.append(v)

			##remove the edges from i to v
			T[u][v] = 0
			T[v][u] = 0

			##reset u to the start of the list
			u = 0
		else:
			u = u + 1
	return P

# a = [(1,2), (2,1), (4,3), (3,4)]
# print(get_ties(a))

u = tree_to_dict([1,2,2], 3)
print(get_adj(u, 3))
v = tree_to_dict([1,2,2,2,2,1], 4)
print(get_adj(v, 4))