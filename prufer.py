import numpy as np

##use Prufer sequence to generate trees
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
def genTree(l, eq):
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

def leafnNode(T,d,u,v,w,l):
	##v is the leaf, w is the internal node
	##set the length to the leaf
		d[u][v] = l
		d[v][u] = l

		##set the length from u to w to be a random number less than l
		lr = np.random(l)
		d[u][w] = lr
		d[w][u] = lr

		##and recurse to find the lengths from the other node
		return findLengths(T,d,w,l-lr)

def findLengths(T,d,u,l):
	##if T is the zero matrix we're done, so return the distances
	if np.count_nonzero(T) == 0:
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
	deg_v = T[v].count[1]
	deg_w = T[w].count[1]

	##remove the edges to u
	T[u][v] = 0
	T[v][u] = 0
	T[u][w] = 0
	T[w][u] = 0

	##case 1: the two other vertices connected to u are leaves
	if deg_v == 1 & deg_w == 1:
		##set the lengths
		d[u][v] = l
		d[v][u] = l
		d[u][w] = l
		d[w][u] = l
		return

	##case 2: the other two vertices connected to u are a leaf and an internal node
	if deg_v == 1 & deg_w == 3:
		return leafnNode(T,d,u,v,w,l)

	if deg_v == 3 & deg_w == 3:
		return leafnNode(T,d,u,w,v,l)
	
	##case 3: both nodes are internal
	##remove the edges to u
	findLengths(T,d,v,l)
	findLengths(T,d,w,l)

##make the trees equidistant
##takes 0 to be the root always
def makeEq(T):
	T_copy = T.copy()
	n = len(T)

	##make a new array to store the distances in
	d = np.zeros((n,n))
	
	##assume first (len(T) + 2)/2 nodes are the leaves
	leaves = [i for i in range(1, (len(T) + 2)/2)]

	##find the internal node connected to 0
	u = -1
	for j in range(len(T)):
		if T[0][j] == 1:
			u = j
			T_copy[0][u] == 0
			T_copy[u][0] == 0
			break

	return findLengths(T,d,u,1)