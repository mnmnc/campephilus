import math
import operator


class LOF2D:

	def __init__(self, points):

		#   points = [
		#       [x, y],
		#       [x, y]
		#   ]

		self.data = points
		self.neighbours = {}
		self.outliers = []
		self.k_distances = {}
		self.lrd = {}
		self.reach_distance_sum = {}
		self.lof = {}
		self.sorted_lof = []

	def create_distance_dictionary(self):
		"""
		Creates a dictionary of distances between all points
		:return:
		"""
		self.neighbours = {}

		# TODO: Optimize this with the use of dynamic programming,
		# TODO: since it calculates same distances twice
		for i in range(len(self.data)-1):
			point = (int(self.data[i][0]),int(self.data[i][1]))
			point_neighbours = {}
			for j in range(len(self.data)-1):
				compared_point = (int(self.data[j][0]), int(self.data[j][1]))
				if i != j:
					if compared_point not in point_neighbours:
						sum = (point[0] - compared_point[0])*(point[0] - compared_point[0]) + (point[1] - compared_point[1]) * (point[1] - compared_point[1])
						result = math.sqrt(sum)
						point_neighbours.update({compared_point:result})
						if compared_point not in self.neighbours:
							compared_point_neighbours = {}
							compared_point_neighbours.update({point:result})
							self.neighbours.update({compared_point:compared_point_neighbours})
						else:
							temp_dict = self.neighbours.get(compared_point)
							temp_dict.update({point:result})
							self.neighbours.update({compared_point:temp_dict})
			self.neighbours.update({point:point_neighbours})

	def print_neighbours(self):
		for key in self.neighbours:
			print("\n",key,"\t:\n")
			for k in self.neighbours[key]:
				print("\t",k,"\t:", self.neighbours[key][k])

	def get_knn(self, k=3):
		"""
		Limits previously created distances dictionary so that it will contain
		only neighbours with distance equal or closer than k neighbour.
		:param k: number that specifies which neighbour distance should designate the threshold
		:return:
		"""
		for key in self.neighbours:
			k_closest = []
			temp_values = []
			for subkey in self.neighbours[key]:
				temp_values.append(self.neighbours[key][subkey])

			temp_values.sort()

			threshold_value = temp_values[k-1]

			for subkey in self.neighbours[key]:
				if self.neighbours[key][subkey] <= threshold_value:
					k_closest.append(subkey)

			selected_dictionary = {}
			for k_closest_neighbour in k_closest:
				for subkey in self.neighbours[key]:
					if k_closest_neighbour == subkey:
						selected_dictionary.update({subkey:self.neighbours[key][subkey]})

			self.k_distances.update({key:selected_dictionary})



	def calculate_lrd(self):
		"""
		Calculates local reachability density for each point.
		Updates LRD dictionary with results.
		:return:
		"""
		for point in self.k_distances:
			neighbours_count = len(self.k_distances[point])

			sum = 0
			for neighbour in self.k_distances[point]:
				biggest = -1
				for inner_neighbour in self.k_distances[neighbour]:
					if self.k_distances[neighbour][inner_neighbour] > biggest:
						biggest = self.k_distances[neighbour][inner_neighbour]


				dist = self.neighbours[neighbour][point]

				if biggest > dist:
					sum += biggest
				else:
					sum += dist

			self.lrd.update({point: neighbours_count/sum})
			self.reach_distance_sum.update({point:sum})

	def calculate_lof(self):
		"""
		Calculates LOF for all points.
		Updates local LOF dictionary with results.
		:return:
		"""
		for point in self.k_distances:
			lrd_sum = 0
			for neighbour in self.k_distances[point]:
				lrd_sum += self.lrd[neighbour]
			self.lof.update({point:lrd_sum * self.reach_distance_sum[point]})

	def sort_lof(self):
		"""
		Sorts LOF data based on LOF value, descendingly
		:return: list of tuples ( (x, y), lof_value )
		"""
		self.sorted_lof = sorted(self.lof.items(), key=operator.itemgetter(1), reverse=True)

	def print_lof(self):
		for ele in self.sorted_lof:
			print("point:", ele[0], "lof:", ele[1])

	def print_k_distances(self):
		for key in self.k_distances:
			print("\n",key,"\t:\n")
			for subkey in self.k_distances[key]:
				print("\t",subkey,"\t:", self.k_distances[key][subkey])

	def get_top(self, number):
		result = []
		for i in range(number):
			result.append(self.sorted_lof[i][0])
		return result

def main():

	neighbours = 3

	points = [
		[1, 2], [2, 4], [3, 6], [4, 37], [5, 2],
		[6, 5], [7, 3], [8, 4], [9, 8]
	]

	lof = LOF2D(points)

	# 1. Calculate all the distances
	lof.create_distance_dictionary()
	#lof.print_neighbours()

	# 2. Get all neighbours that are closer or equal to k neighbour
	lof.get_knn(neighbours)
	#lof.print_k_distances()

	# 3. Calculate local reachability density for all points
	lof.calculate_lrd()

	# 4. Calculate LOF
	lof.calculate_lof()

	# 5. Sort
	lof.sort_lof()

	# 6. Show
	#lof.print_lof()

	# 7. Get top 3
	print(lof.get_top(3))

	import pydoc
	help(lof)


if __name__ == "__main__":
	main()

