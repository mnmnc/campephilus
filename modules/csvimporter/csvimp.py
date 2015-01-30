
from csv import reader

class Csvimp:
	data = []

	def __init__(self, input_file):
		self.input = input_file

	def load_data(self):
		with open(self.input) as input:
			self.data = list(reader(input))

	def set_intput(self, filename):
		self.input = filename

def main():
	pass

if __name__  == "__main__":
	main()
