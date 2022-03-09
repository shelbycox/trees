class Tree():
	def __init__(self, l, w_adj=None):
		##record the number of leaves, vertices, and their indices
		self.num_leaves = l
		self.leaves = [i for i in range(l)]
		self.num_verts = 2*l - 2
		self.verts = [j for j in range(l+1, 2*l - 2)]

		##record the weighted adjacency matrix
		self.w_adj = w_adj.copy()

		##if there's no given adjacency matrix, then make one
		if self.w_adj is None:
			self.w_adj = np.zeros((2*l - 2, 2*l - 2))
			self.adj = np.zeros((2*l - 2, 2*l - 2))

		else:
			self.adj = np.array([[w_adj[i][j] != 0 for i in range(len(w_adj))] for j in range(len(w_adj))])

