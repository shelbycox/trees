import numpy as np
import networkx as nx
from decimal import *

##gets a random decimal from the interval [a,b]
def rand_dec(a,b,digits=7):
	f = round(np.random.uniform(a,b), digits)

	return Decimal(str(f))

def get_prufer(T):
	##P will hold the Prufer sequence
	P = []
	
	##u is a counting variable
	u = 0
	while u < len(T):
		##if u is a leaf (has exactly one adjacent vertex)
		if np.count_nonzero(T[u]) == 1:
			##v will be the vertex adjacent to u
			for i in range(len(T)):
				if T[u][i] != 0:
					v = i
					break
			
			##add v to the Prufer sequence
			P.append(v)
			
			##remove the edge between u and v from T
			T[u][v], T[v][u] = 0, 0
			
			##start checking for leaves again, at the beginning of the list
			u = 0
		
		else:
			##if u is not a leaf, move on
			u = u + 1
	
	return P

def build_tree(a):
	##n is the total number of leaves
	n = len(a) + 2
	
	##make a list that records the degree of each vertex
	deg = [1 + a.count(i) for i in range(n)]
	
	##T will store the adjacency matrix of the tree
	T = np.zeros((n, n))
	
	##starting with the lowest numbered leaf, add an edge to the vertices given by the Prufer sequence
	for i in a:
		for j in range(n):
			if deg[j] == 1:
				T[i][j] = 1
				T[j][i] = 1
				deg[j] = deg[j] - 1
				deg[i] = deg[i] - 1
				break
	
	##now there are just two vertices with positive degree remaining
	u = -1
	v = -1
	for i in range(n):
		if deg[i] == 1:
			if u == -1:
				u = i
			else:
				v = i
				break
	
	T[u][v], T[v][u] = 1, 1
	
	return T

def gen_tri_tree(l, eq=True):
	##n stores the total number of vertices in the tree
	##a trivalent tree has l - 2 internal vertices, where l is the number of leaves
	n = l + (l - 2)
	
	##the leaves are the first l numbers, internal vertices are the last l - 2
	leaves = [i for i in range(l)]
	internal = [i for i in range(l, n)]
	
	##in a trivalent tree, each internal vertex appears in the Prufer sequence exactly twice
	##the leaves don't appear at all
	perm = np.random.permutation(range(2*len(internal)))
	a = [internal[int(p/2)] for p in perm]
	
	##now build the tree from the Prufer sequence we generated
	T = build_tree(a)
	
	##if the tree needs to be equidistant, make it equidistant
	if eq:
		return make_eq(T)
	
	##otherwise just return T
	return T

def make_eq(T):
	##make a copy of the adjacency matrix
	##we will use this to record the edges we have already checked
	T_copy = T.copy()
	##store the number of vertices
	n = len(T)
	
	##d will store the weighted adjacency matrix
	d = np.zeros((n, n))
	
	##assumes the first (len(T) + 2)/2 vertices are the leaves
	leaves = [i for i in range(1, int((n + 2)/2))]
	
	##find the internal node connected to 0
	u = -1
	for j in range(len(T)):
		if T[0][j] == 1:
			u = j
			##remove the edge between 0 and u
			T_copy[0][u], T_copy[u][0] == 0, 0
			break
	
	d = find_lengths(T_copy, d, u, 1)
	
	##add the edges back to 0
	##this ensures the tree is trivalent, but 0 is the root of the tree
	d[0][u], d[u][0] = 1, 1
	
	return d

def find_lengths(T, d, u, l):
	##T keeps track of edges we haven't visited
	##if T is all zeros, then we've visited all edges, so we're done
	if np.count_nonzero(T) == 0:
		return d
	
	##otherwise, get the two nodes connected to u
	v = -1
	w = -1
	for j in range(len(T)):
		##do I need to worry about loops?
		if T[u][j] == 1 and j != u:
			if v == -1:
				v = j
			else:
				w = j
				break
	
	##get the degrees of the vertices connected to u
	deg_v = np.count_nonzero(T[v])
	deg_w = np.count_nonzero(T[w])
	
	##remove the edges to u
	T[u][v], T[v][u], T[u][w], T[w][u] = 0, 0, 0, 0
	
	##CASE 1: v, w are leaves
	if deg_v == 1 and deg_w == 1:
		d[u][v], d[v][u], d[u][w], d[w][u] = l, l, l, l
		return d
	
	##CASE 2: v is a leaf and w is internal
	elif deg_v == 1 and deg_w == 3:
		d[u][v], d[v][u] = l, l
		
		lr = rand_dec(0, l)
		d[u][w], d[w][u] = lr, lr
		
		return find_lengths(T, d, w, l-lr)
	
	##CASE 3: v is internal and w is a leaf
	elif deg_v == 3 and deg_w == 1:
		d[u][w], d[w][u] = l
		
		lr = rand_dec(0, l)
		d[u][v], d[v][u] = lr, lr
		
		return find_lengths(T, d, v, l-lr)
	
	##CASE 4: both v and w are internal nodes
	elif deg_v == 3 and deg_w == 3:
		l1 = rand_dec(0, l)
		d[u][v], d[v][u] = l1, l1
		
		l2 = rand_dec(0, l)
		d[u][w], d[w][u] = l2, l2
		
		d = find_lengths(T, d, v, l-l1)
		return find_lengths(T, d, w, l-l2)

def get_dist(D, i, j, d):
	##if we reached j, we're done
	if i == j:
		return d
	
	##n stores the number of vertices
	n = len(D)
	
	##get a list of the vertices adjacent to i
	adjacent = [k for k in range(n) if D[i][k] != 0]
	
	##if we reached a leaf that's not j, we can't go any further
	if len(adjacent) == 0:
		return -1
	
	temp_dist = D[i].copy()
	for k in adjacent:
		D[i][k], D[k][i] = 0, 0
		
	return max([get_dist(D, k, j, d + temp_dist[k]) for k in adjacent])

def get_metric(D):
	##n stores the total number of vertices
	n = len(D)
	
	##a trivalent tree has (n + 2)/2 leaves
	num_leaves = int((n + 2)/2)
	
	##the dictionary u stores the metric
	u = dict()
	
	for i in range(num_leaves):
		for j in range(i+1, num_leaves):
			dij = get_dist(D.copy(), i, j, 0)
			u[(i,j)] = dij
			u[(j,i)] = dij
	
	return u

def sameEdges(R,T):
	if len(R) != len(T):
		return False

	for i in range(1,len(R)):
		for j in range(1,len(R)):
			if R[i][j] != 0:
				if T[i][j] == 0:
					print('Error 1!', i, j)
					return False
			elif R[i][j] == 0:
				if T[i][j] != 0:
					print('Error 2! ', i, j)
					return False

	return True

def convertToNetworkX(tree):
	edges = []
	for i in range(len(tree)):
		for j in range(len(tree)):
			if tree[i][j] != 0:
				edges.append((i,j))
	##encode the adjacency matrix as a graph
	G = nx.Graph()
	G.add_edges_from(edges)
	return G