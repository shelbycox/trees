import unittest
from prufer import *

class TestPruferToTree(unittest.TestCase):
	a = [4,4,5,5]
	b = [4,5,4,5]
	c = [6,6,7,7,8,8,9,9]
	d = [6,6,7,8,9,9,7,8]
	n_verts = [6, 6, 10, 10]

	trees = []
	for t in [a,b,c,d]:
		trees.append(buildTree(t))

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

if __name__ == '__main__':
    unittest.main()