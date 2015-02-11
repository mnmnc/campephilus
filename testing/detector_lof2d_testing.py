
import sys; import os
sys.path.insert(0, os.path.abspath('..'))
from modules.detector import lof2d
import unittest

class LOF2DTestCase(unittest.TestCase):

	points = [
		[1, 2], [2, 4], [3, 6], [4, 37], [5, 2],
		[6, 5], [7, 3], [8, 4], [9, 8]
	]
	neighbours = 3

	lof_test = lof2d.LOF2D(points)

	def test_lof_operation(self):

		# 1. Calculate all the distances
		self.lof_test.create_distance_dictionary()

		# 2. Get all neighbours that are closer or equal to k neighbour
		self.lof_test.get_knn(self.neighbours)

		# 3. Calculate local reachability density for all points
		self.lof_test.calculate_lrd()

		# 4. Calculate LOF
		self.lof_test.calculate_lof()

		# 5. Sort
		self.lof_test.sort_lof()

		top_3 = self.lof_test.get_top(3)

		correct = 0

		error = ""

		result_1 = (4, 37)
		result_2 = (3, 6)
		result_3 = (6, 5)

		if top_3[0] == result_1:
			correct += 1
		else:
			error += "\tExpected (" + str(result_1[0]) + ", " + str(result_1[1]) + ") instead of (" + str(top_3[0][0]) + ", " + str(top_3[0][1]) + ").\n"
		if top_3[1] == result_2:
			correct += 1
		else:
			error += "\tExpected (" + str(result_2[0]) + ", " + str(result_2[1]) + ") instead of (" + str(top_3[1][0]) + ", " + str(top_3[1][1]) + ").\n"
		if top_3[2] == result_3:
			correct += 1
		else:
			error += "\tExpected (" + str(result_3[0]) + ", " + str(result_3[1]) + ") instead of (" + str(top_3[2][0]) + ", " + str(top_3[2][1]) + ").\n"

		self.assertEqual(correct, 3, "LOF gives unexpected results.\n" + error)

	def test_other_operation(self):
		self.assertEqual(1, 1)



if __name__ == '__main__':
	unittest.main(verbosity=2)
