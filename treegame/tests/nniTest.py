import tropicalLines as tl
import numpy as np

u = {(1, 2): 40, (2, 1): 40, (1, 3): 40, (3, 1): 40, (1, 4): 40, (4, 1): 40, (1, 5): 40, (5, 1): 40, (2, 3): 30, (3, 2): 30, (2, 4): 30, (4, 2): 30, (2, 5): 30, (5, 2): 30, (3, 4): 20, (4, 3): 20, (3, 5): 20, (5, 3): 20, (4, 5): 10, (5, 4): 10}
v = {(1, 2): 1, (2, 1): 1, (1, 3): 2, (3, 1): 2, (1, 4): 3, (4, 1): 3, (1, 5): 4, (5, 1): 4, (2, 3): 2, (3, 2): 2, (2, 4): 3, (4, 2): 3, (2, 5): 4, (5, 2): 4, (3, 4): 3, (4, 3): 3, (3, 5): 4, (5, 3): 4, (4, 5): 4, (5, 4): 4}

a = {(1, 2): -166.0, (2, 1): -166.0, (1, 3): 2.0, (3, 1): 2.0, (1, 4): -26.0, (4, 1): -26.0, (1, 5): -26.0, (5, 1): -26.0, (2, 3): 2.0, (3, 2): 2.0, (2, 4): -26.0, (4, 2): -26.0, (2, 5): -26.0, (5, 2): -26.0, (3, 4): 2.0, (4, 3): 2.0, (3, 5): 2.0, (5, 3): 2.0, (4, 5): -164.0, (5, 4): -164.0}
b = {(1, 2): 2.0, (2, 1): 2.0, (1, 3): 2.0, (3, 1): 2.0, (1, 4): -164.0, (4, 1): -164.0, (1, 5): 2.0, (5, 1): 2.0, (2, 3): -62.0, (3, 2): -62.0, (2, 4): 2.0, (4, 2): 2.0, (2, 5): -62.0, (5, 2): -62.0, (3, 4): 2.0, (4, 3): 2.0, (3, 5): -194.0, (5, 3): -194.0, (4, 5): 2.0, (5, 4): 2.0}

line = tl.get_tropical_line(a,b)

# adj_u = tl.get_adj(u, 5)
# adj_v = tl.get_adj(v, 5)

# print(adj_u)
# print(adj_v)

# print(tl.get_prufer(adj_u))
# print(tl.get_prufer(adj_v))

# for l in line:
# 	A = tl.get_adj(l,5)
# 	for a in range(len(A)):
# 		if np.count_nonzero(A[a]) not in [1,3]:
# 			print('Non Generic')
# 			print(A)
	# print(tl.get_adj(l, 5))
	# print(l, tl.get_prufer(tl.get_adj(l, 5))[:-1], tl.contribution(l, 5))

##prufer probably ok, adj not working as expected (vertices with degree too high!)
##I think get_adj is working now

##for the benefit of get_prufer, maybe I should have get_adj add the root
##will simplify contribution calculution

print(tl.get_adj(line[3], 5))