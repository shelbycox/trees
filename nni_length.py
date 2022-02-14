from tropicalLines import *

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