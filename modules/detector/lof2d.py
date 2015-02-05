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

	def create_distance_dictionary(self):
		distances = {}
		self.neighbours = {}

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

		# for key in self.neighbours:
		# 	print("\n",key,"\t:\n")
		# 	for k in self.neighbours[key]:
		# 		print("\t",k,"\t:", self.neighbours[key][k])

	def get_knn(self, k=3):

		for key in self.neighbours:
			k_closest = []
			temp_values = []
			for subkey in self.neighbours[key]:
				temp_values.append(self.neighbours[key][subkey])


			temp_values.sort()
			#print(temp_values)

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

		for key in self.k_distances:
			print("\n",key,"\t:\n")
			for subkey in self.k_distances[key]:
				print("\t",subkey,"\t:", self.k_distances[key][subkey])


def main():



	points = [
		[1, 2], [2, 4], [3, 6], [4, 37], [5, 2],
		[6, 5], [7, 3], [8, 4], [9, 8]
	]

	lof = LOF2D(points)

	lof.create_distance_dictionary()
	lof.get_knn(3)

if __name__ == "__main__":
	main()

