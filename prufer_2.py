import numpy as np
import networkx as nx
from decimal import *
##rounding digits
digits = 6
##for testing
count = 0

##gets a random decimal from the interval [a,b]
def rand_dec(a,b,digits=7):
	f = np.random.uniform(a,b)

	return Decimal(str(f))

##given the adjacency matrix for a tree, find the Prufer sequence
def getPrufer(T):
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

##use Prufer sequence to generate trees
##TESTED
def buildTree(a):
	n = len(a) + 2

	##make a list that records degrees
	deg = [1 + a.count(i) for i in range(n)]

	##make an empty adjacency matrix for the tree
	T = np.zeros((n, n))

	##starting with the lowest numbered degree 1 vertex, add an edge to the vertices in the Prufer sequence
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
	T[u][v] = 1
	T[v][u] = 1

	##return the adjacency matrix T
	return T

##generate a random trivalent tree on l leaves
##TESTED
def genTree(l, eq=True):
	##a trivalent tree on n leaves has n-2 internal vertices
	n = l + (l - 2)

	leaves = [i for i in range(l)]
	internal = [i for i in range(l, n)]

	##each internal vertex should appear twice in the Prufer sequence
	perm = np.random.permutation(range(2*len(internal)))
	a = [internal[int(p/2)] for p in perm]

	T = buildTree(a)

	if eq:
		return makeEq(T)

	return T

##TESTED
def findLengths(T,d,u,l):
	##if T is the zero matrix we're done, so return the distances
	if np.count_nonzero(T) == 0:
		#print('T is zero! ', d)
		return d

	##get the two other vertices connected to u
	v = -1
	w = -1
	for j in range(len(T)):
		if T[u][j] == 1 and j != u:
			if v == -1:
				v = j
			else:
				w = j
				break

	##get the degrees of those vertices
	deg_v = np.count_nonzero(T[v])
	deg_w = np.count_nonzero(T[w])
	#print('deg(v), deg(w) are: ', deg_v, deg_w)

	##remove the edges to u
	T[u][v] = 0
	T[v][u] = 0
	T[u][w] = 0
	T[w][u] = 0

	##case 1: the two other vertices connected to u are leaves
	if deg_v == 1 and deg_w == 1:
		##set the lengths to the two leaves
		#print('in first case')
		d[u][v] = l
		d[v][u] = l
		d[u][w] = l
		d[w][u] = l
		return d

	##case 2: the other two vertices connected to u are a leaf and an internal node
	elif deg_v == 1 and deg_w == 3:
		##v is the leaf, w is the internal node
		##set the length to the leaf
		#print('set length to v')
		d[u][v] = l
		d[v][u] = l

		##set the length from u to w to be a random number less than l
		#print('set length to w')
		lr = rand_dec(0,l)
		d[u][w] = lr
		d[w][u] = lr

		#print(d)

		##and recurse to find the lengths from the other node
		#print('recursing')
		return findLengths(T,d,w,l-lr)

	elif deg_v == 3 and deg_w == 1:
		##w is the leaf, v is the internal node
		##set the length to the leaf
		d[u][w] = l
		d[w][u] = l

		##set the length from u to v to be a random number less than l
		lr = rand_dec(0,l)
		d[u][v] = lr
		d[v][u] = lr

		##and recurse to find the lengths from the other node
		return findLengths(T,d,v,l-lr)
	
	##case 3: both nodes are internal
	elif deg_v == 3 and deg_w == 3:
		##set the length to v
		l1 = rand_dec(0,l)
		d[u][v] = l1
		d[v][u] = l1

		##set the length to w
		l2 = rand_dec(0,l)
		d[u][w] = l2
		d[w][u] = l2

		##recurse
		d = findLengths(T,d,v,l-l1)
		return findLengths(T,d,w,l-l2)

##make the trees equidistant
##takes 0 to be the root always
##TESTED
def makeEq(T):
	T_copy = T.copy()
	n = len(T)

	##make a new array to store the distances in
	d = np.zeros((n,n))
	
	##assume first (len(T) + 2)/2 nodes are the leaves
	leaves = [i for i in range(1, int((n + 2)/2))]

	##find the internal node connected to 0
	u = -1
	for j in range(len(T)):
		if T[0][j] == 1:
			u = j
			T_copy[0][u] = 0
			T_copy[u][0] = 0
			break

	d = findLengths(T_copy,d,u,1)
	##add back the edges to 0
	d[0][u] = 1
	d[u][0] = 1

	return d

##given a metric tree D and two vertices, i and j, finds the distnace between them
##TESTED
def getDist(D,i,j,d):
	#print('i, j are: ', i, j)

	##if we reached j, then return the current distance
	if i == j:
		#print('found the distance! ', d)
		return d

	##get the number of vertices
	n = len(D)

	##get the degree of i
	deg_i = np.count_nonzero(D[i])

	##get a list of the vertices adjacent to i
	adjacent = [k for k in range(n) if D[i][k] != 0]
	#print('the vertices adjacent to i are: ', adjacent)

	if len(adjacent) == 0:
		return -1

	##otherwise, recurse to find a path to j
	##store the distances temporarily
	temp_dist = D[i].copy()
	##remove the edges we just used
	for k in adjacent:
		D[i][k] = 0
		D[k][i] = 0
		#print('the new distance is:', d + temp_dist[k])

	return max([getDist(D,k,j,d + temp_dist[k]) for k in adjacent])

##given a trivalent tree with edges labelled with lengths, return the tree metric as a vector
##TESTED
def getMetric(D):
	##get the total number of vertices
	n = len(D)
	##get the indices of the leaves, assuming they are first
	l = int((n + 2)/2)

	##the dicitonary u will store the metric
	u = dict()

	for i in range(l):
		for j in range(i+1,l):
			dij = getDist(D.copy(),i,j,0)
			u[(i,j)] = dij
			u[(j,i)] = dij

	return u

##TESTED
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

##TESTED
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