import unittest
from tropicalLines import *

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

def symmetrize(l):
	new_l = []
	for (i,j) in l:
		new_l.append((i,j))
		new_l.append((j,i))
	return new_l

def symmetrize_ll(L):
	new_L = []
	for l in L:
		new_L.append(symmetrize(l))

	return new_L

T1 = tree_to_dict([4,4,2], 3)
T2 = tree_to_dict([2,4,4], 3)
T3 = tree_to_dict([1,4,4,4,4,2], 4)
T4 = tree_to_dict([2,1,2,2,1,2], 4)
test_trees = [T1, T2, T3, T4]
test_args = [argmaxm(t) for t in test_trees]
lens = [2,2,3,2]

arg_1 = symmetrize_ll([[(1,2), (1,3)], [(2,3)]])
arg_2 = symmetrize_ll([[(1,3), (2,3)], [(1,2)]])
arg_3 = symmetrize_ll([[(1,3), (1,4), (2,3), (2,4)], [(3,4)], [(1,2)]])
arg_4 = symmetrize_ll([[(1,2), (1,4), (2,3), (3,4)], [(1,3), (2,4)]])
known_args = [arg_1, arg_2, arg_3, arg_4]

class TestArgmaxm(unittest.TestCase):
	##pick some representative trees
	##including ones with internal ties

	def test_arg_len(self):
		for i in range(len(test_trees)):
			self.assertEqual(len(test_args[i]), lens[i])

	def test_arg(self):
		for i in range(len(test_args)):
			test = test_args[i]
			known = known_args[i]
			for j in range(len(test)):
				try:
					self.assertEqual(set(test[j]), set(known[j]))

				except IndexError:
					print('arg is the wrong length')

class TestNormalizeHeights(unittest.TestCase):
	##generate some trees
	##pick some heights to normalize to
	test_heights = [-1, 0, 1, 3, 100]
	
	##check that the new trees are the correct height
	def test_total_height(self):
		for h in self.test_heights:
			r_trees = normalize_heights(test_trees, h)
			for t in range(len(r_trees)):
				reps = argmaxm(r_trees[t])[0]
				for r in reps:
					self.assertEqual(r_trees[t][r], h)


	##tests to make sure the (fine) structure of the tree is unchanged
	def test_arg_unchanged(self):
		for h in self.test_heights:
			r = normalize_heights(test_trees, h)
			for t in range(len(r)):
				test = argmaxm(r[t])
				known = known_args[t]
				for j in range(len(test)):
					self.assertEqual(set(test[j]), set(known[j]))

class TestGetTropicalLine(unittest.TestCase):
	##not sure what to do for this one...
	pass

class TestCompareTrees(unittest.TestCase):
	##not sure what to do here either....
	##maybe do some trees with 6 leaves
	##and trees with same structure but different numbers
	
	##check that all the known trees are different
	def test_different(self):
		for i in range(len(test_trees)):
			for j in range(i+1, len(test_trees)):
				self.assertFalse(compare_trees(test_trees[i], test_trees[j]))

	##check that all the known trees are the same as themselves
	def test_same(self):
		for t in test_trees:
			self.assertTrue(compare_trees(t, t))

class TestReduceLine(unittest.TestCase):
	##use compare_trees to see if any of the trees are the same for some random examples
	##come up with some examples where I know the answer
	pass

class TestGetLineInt(unittest.TestCase):
	##do a few small known examples
	##make sure the numbers are in order for larger random examples
	pass

class TestLeftRightSplit(unittest.TestCase):
	##get some examples on around ~10 leaves where I know the answer
	pass

class TestTreeRest(unittest.TestCase):
	##no idea what to do here
	pass

class TestRecTreeParen(unittest.TestCase):
	##do some small cases that I know here
	##no idea what else to do
	pass

class TestSplit(unittest.TestCase):
	##do some small known examples
	pass

class TestPrintPath(unittest.TestCase):
	##no idea what to do here, do I need to test this?
	pass

class TestGetFineCodim(unittest.TestCase):
	##do some known examples
	##star tree, generic tree for different numbers of leaves
	pass

class TestGetCoarseCodim(unittest.TestCase):
	##do some known examples
	##star tree, generic tree for different numbers of leaves
	pass

class TestAllPaires(unittest.TestCase):
	##do some small known examples
	##test that it gets the right list of elements also
	pass

class TestGetHeights(unittest.TestCase):
	##do some small knwon examples
	##confirm there are the correct number of heights for star tree, generic trees, some in between
	pass

if __name__ == '__main__':
    unittest.main()