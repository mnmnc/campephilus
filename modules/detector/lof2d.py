import math

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

	def create_distance_dictionary(self):
		"""
		Creates a dictionary of distances between all points
		:return:
		"""
		self.neighbours = {}

		# TODO: Optimize this with the use of dynamic programming,
		# TODO: since it calculates same distances twice
		for i in range(len(self.data)-1):
			point = (self.data[i][0],self.data[i][1])
			point_neighbours = {}
			for j in range(len(self.data)-1):
				compared_point = (self.data[j][0], self.data[j][1])
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
			print(key,", threashold: ", threshold_value)

			for subkey in self.neighbours[key]:
				if self.neighbours[key][subkey] <= threshold_value:
					k_closest.append(subkey)

			selected_dictionary = {}
			for k_closest_neighbour in k_closest:
				for subkey in self.neighbours[key]:
					if k_closest_neighbour == subkey:
						selected_dictionary.update({subkey:self.neighbours[key][subkey]})

			self.k_distances.update({key:selected_dictionary})

	def print_k_distances(self):
		for key in self.k_distances:
			print("\n",key,"\t:\n")
			for subkey in self.k_distances[key]:
				print("\t",subkey,"\t:", self.k_distances[key][subkey])

	def calculate_lrd(self):
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
		for point in self.k_distances:
			lrd_sum = 0
			for neighbour in self.k_distances[point]:
				lrd_sum += self.lrd[neighbour]
			print("LOF", point, lrd_sum * self.reach_distance_sum[point])

def main():

	neighbours = 3

	points = [
		[1, 2], [2, 4], [3, 6], [4, 37], [5, 2],
		[6, 5], [7, 3], [8, 4], [9, 8]
	]

	lof = LOF2D(points)

	# 1. Calculate all the distances
	lof.create_distance_dictionary()

	lof.print_neighbours()

	# 2. Get all neighbours that are closer or equal to k neighbour
	lof.get_knn(neighbours)

	lof.print_k_distances()

	# 3. Calculate local reachability density for all points

	lrd = {}
	reachdist_sum = {}

	# FOR [1, 2] - first point
	for t_point in lof.k_distances:
		# Get number of neighbours
		point_neighbours_count = len(lof.k_distances[t_point])
		#print("Neighbours count:", point_neighbours_count)

			# For each neighbour calculate reachdist
				# maximum from
				#               distance from neighbour to its k neighbour
				#               or
				#               distance from neighbour to original point
		sum = 0
		for point in lof.k_distances[t_point]:
			#print("Calculating reachdist for", point)

			biggest = -1
			for neighbour in lof.k_distances[point]:
				if lof.k_distances[point][neighbour] > biggest:
					biggest = lof.k_distances[point][neighbour]

			#print("\tBiggest:", biggest )

			dist = lof.neighbours[point][t_point]

			#print("\tDistance", point, "to", t_point, ":", dist)

			if biggest > dist:
				sum += biggest
			else:
				sum += dist


		#print("Sum: ", sum)
		print("LRD of ", t_point , ":", point_neighbours_count/sum)
		lrd.update({t_point: point_neighbours_count/sum})
		reachdist_sum.update({t_point:sum})

	lof.calculate_lrd()

	# 4. Calculate LOF

	for t_point in lof.k_distances:
		#print("LOF", t_point)
		lrd_sum = 0
		for neighbour in lof.k_distances[t_point]:
			#print("\tNeighbour", neighbour, "lrd", lrd[neighbour])
			lrd_sum += lrd[neighbour]
		#print("\tSum", reachdist_sum[t_point])
		print("LOF", t_point, lrd_sum * reachdist_sum[t_point])

	lof.calculate_lof()

	# 5. Sort


if __name__ == "__main__":
	main()

