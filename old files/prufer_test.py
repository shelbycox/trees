import unittest
from prufer_2 import *
import networkx as nx

##checking buildTree, which turns a Prufer sequence into a tree
class TestPruferToTree(unittest.TestCase):
	a = [4,4,5,5]
	b = [4,5,4,5]
	c = [6,6,7,7,8,8,9,9]
	d = [6,6,7,8,9,9,7,8]
	n_verts = [6, 6, 10, 10]

	trees = []
	for t in [a,b,c,d]:
		trees.append(build_tree(t))

	##TEST 1: just make sure the number of vertices is as expected
	def testNumVert(self):
		for i in range(len(self.trees)):
			self.assertEqual(len(self.trees[i]),self.n_verts[i])


	T_a = np.array([[0,0,0,0,1,0], 
					[0,0,0,0,1,0], 
					[0,0,0,0,0,1], 
					[0,0,0,0,0,1],
					[1,1,0,0,0,1],
					[0,0,1,1,1,0]])

	T_b = np.array([[0,0,0,0,1,0], 
					[0,0,0,0,0,1], 
					[0,0,0,0,1,0], 
					[0,0,0,0,0,1],
					[1,0,1,0,0,1],
					[0,1,0,1,1,0]])

	T_c = np.array([[0,0,0,0,0,0,1,0,0,0],
					[0,0,0,0,0,0,1,0,0,0],
					[0,0,0,0,0,0,0,1,0,0],
					[0,0,0,0,0,0,0,1,0,0],
					[0,0,0,0,0,0,0,0,1,0],
					[0,0,0,0,0,0,0,0,1,0],
					[1,1,0,0,0,0,0,0,0,1],
					[0,0,1,1,0,0,0,0,0,1],
					[0,0,0,0,1,1,0,0,0,1],
					[0,0,0,0,0,0,1,1,1,0]])

	T_d = np.array([[0,0,0,0,0,0,1,0,0,0],
					[0,0,0,0,0,0,1,0,0,0],
					[0,0,0,0,0,0,0,1,0,0],
					[0,0,0,0,0,0,0,0,1,0],
					[0,0,0,0,0,0,0,0,0,1],
					[0,0,0,0,0,0,0,0,0,1],
					[1,1,0,0,0,0,0,1,0,0],
					[0,0,1,0,0,0,1,0,1,0],
					[0,0,0,1,0,0,0,1,0,1],
					[0,0,0,0,1,1,0,0,1,0]])

	S = [T_a, T_b, T_c, T_d]

	##TEST 2: actually check the structure of the adjacency matrix
	def testStucture(self):
		for i in range(len(self.trees)):
			self.assertTrue(np.array_equal(self.S[i], self.trees[i]), i)

##checking that genTree actually generates a trivalent tree with the right number of vertices
class randomTreeTest(unittest.TestCase):
	R = gen_tri_tree(4, eq=False)
	S = gen_tri_tree(6, eq=False)
	T = gen_tri_tree(7, eq=False)

	testTrees = [gen_tri_tree(i) for i in range(5,100)]
	leaves = [i for i in range(5,100)]
	vert = [i - 2 for i in range(5,100)]

	def testVertexDeg(self):
		for tree in self.testTrees:
			for i in range(len(tree)):
				self.assertTrue(np.count_nonzero(tree[i]) == 1 or np.count_nonzero(tree[i]) == 3, 'all vertices should have degree 1 or 3')

	def testNumLeaves(self):
		for j in range(len(self.testTrees)):
			tree = self.testTrees[j]
			count_leaves = 0
			for i in range(len(tree)):
				if np.count_nonzero(tree[i]) == 1:
					count_leaves = count_leaves + 1
			self.assertTrue(count_leaves == self.leaves[j], 'found ' + str(count_leaves) + ' leaves, should be ' + str(self.leaves[j]))

	def testNumInternalVert(self):
		for j in range(len(self.testTrees)):
			tree = self.testTrees[j]
			count_verts = 0
			for i in range(len(tree)):
				if np.count_nonzero(tree[i]) == 3:
					count_verts = count_verts + 1
			self.assertTrue(count_verts == self.vert[j], 'found ' + str(count_verts) + ' internal vertices, should be ' + str(self.vert[j]))

	def testIsConnected(self):
		for tree in self.testTrees:
			edges = []
			for i in range(len(tree)):
				for j in range(len(tree)):
					if tree[i][j] != 0:
						edges.append((i,j))
			G = nx.Graph()
			G.add_edges_from(edges)
			self.assertTrue(nx.is_connected(G))

	def testTreeness(self):
		for tree in self.testTrees:
			##convert the adjacency matrix into a networkx graph object
			G = convertToNetworkX(tree)
			##this actually checks connectivity also
			self.assertTrue(nx.is_tree(G))

class TestEquidistant(unittest.TestCase):
	start = 5
	N = 50
	testTrees = [gen_tri_tree(i, eq=False) for i in range(start,N)]
	testEqTrees = [make_eq(tree) for tree in testTrees]
	metrics = [get_metric(eq) for eq in testEqTrees]

	##tests to make sure edges are in the right places
	def testEdges(self):
		for i in range(self.N - self.start):
			tree = self.testTrees[i]
			eq = self.testEqTrees[i]
			self.assertTrue(sameEdges(tree, eq), str(tree) + '\n' + str(eq))

	##make sure the distances are assigned to make the tree equidistant
	##from the vertex zero by defualt
	def testDistances(self):
		for i in range(self.N - self.start):
			eq = self.testEqTrees[i]
			for j in range(1, i + self.start):
				self.assertTrue(self.metrics[i][(0,j)] - 2 < 0.00001, i)

	##make sure that the metric is symmetric
	def testSymmetry(self):
		for i in range(self.N - self.start):
			eq = self.testEqTrees[i]
			for j in range(i + self.start):
				for k in range(j + 1, i + self.start):
					self.assertTrue(self.metrics[i][(j,k)] == self.metrics[i][(k,j)])

if __name__ == '__main__':
    unittest.main()