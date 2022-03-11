##consider argmaxm as the list of heights of internal vertices
##what to do about multiplicity?

##can use prufer sequence to get structure of tree
##starting with leaves, get the other leaf(s) with min distance
##what to do about codim?

##how to compute coarse codim?

##put tools all together (into a package?)

##STEP 1: print leaves along the bottom in the order they appear in the paren structure

##STEP 2: find internal vertices, and draw them at the correct height, position
##	idea: record in the internal vertices the leaves/other interal vertices they occur between, then recursively find their x coordinates

##STEP 3: connect the internal vertices to the leaves

##OR use networkx package!

##STEP 1: Get Prufer sequence

import tropicalLines as tl

##given a tree as a metric u (on pairs of leaves), find the Prufer sequence
# def prufer_from_metric(u):
# 	##get the leaves of the tree
# 	leaves = list(set([i for (i,j) in u.keys()]))

# 	u_copy = u.copy()

# 	P = []
# 	while len(P) < len(leaves) - 2:
# 		##get the smallest leaf
# 		i = min(leaves)

# 		##find the other leaf closet to i
# 		j = -1
# 		min_dist = -1
# 		for k in leaves:
# 			if u[(i,k)] < min_dist or min_dist == -1:
# 				min_dist = u[(i,k)]
# 				j = k

# 	pass

# def get_edges(u):
# 	##get the list of leaves
# 	leaves = list(set([i for (i,j) in u.keys()]))

# 	##can we use argmax to get the internal vertices?
# 	for a in reversed(argmax(u)):
# 	##how do we know the degree of an internal vertex?
# 		if len(a) == 2:
# 			pass

def get_leaf(L):
	if type(L) == int:
		return L

	for l in L:
		if type(l) == int:
			return(l)

	return get_leaf(sum([l for l in L], []))

# def draw_graph(u):
# 	structure = recTreeParen(u)
# 	verts = leaves

def get_height(u, structure):
	left_vert = get_leaf(structure[0])
	right_vert = get_leaf(structure[1])

	return tl.get_heights(u).index(u[(left_vert, right_vert)])

def rec_vertices(u, center_x, structure, radius, prev, verts, edges):
	##edge cases: if the current vertex is a leaf
	if type(structure) == int or len(structure) == 1:
		if type(structure) != int:
			structure = structure[0]
		curr = (center_x, -1, structure)

		##record the center vertex at (center_x, center_y)
		verts.append(curr)

		##record a line from the previous to the current vertex
		if prev != None:
			edges.append((prev, curr))

		return verts, edges

	else:
		##get the list of splits
		splits = structure

		##get the height of the center vertex
		# print(get_height(u, structure))
		n = max([i for (i,j) in u.keys()])
		center_y = 245 - (250/n)*(get_height(u, structure))
		if prev == None:
			center_y = 245 - 200
		curr = (center_x, center_y)

	##record the center vertex at (center_x, center_y)
	verts.append(curr)

	##record a line from the previous to the current vertex
	if prev != None:
		edges.append((prev, curr))

	for s in range(len(splits)):
		verts, edges = rec_vertices(u, center_x + (- len(splits)/4 + s)*(2*radius/len(splits)), splits[s], radius/len(splits), curr, verts, edges)

	return verts, edges

# import sys
# print(sys.executable)

# import networkx as nx
# import matplotlib.pyplot as plt

# edge_list = [(1,5), (2,5), (3,6), (4,6), (5,7), (6,7)]
# H = nx.from_edgelist(edge_list)
# nx.draw(H)

# G = nx.complete_graph(5)
# #nx.draw(G)
# plt.show()