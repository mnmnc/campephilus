
class Tshark:

	fields = ""
	filter = ""
	execution_command = ""

	def __init__(self, exe_path, in_path, out_path):
		self.input_path = in_path
		self.output_path = out_path
		self.exec_path = exe_path


		self.network_fields_names = {
			"ip" : {
				"src": " -e ip.src",
			    "dst": " -e ip.dst",
			    "ttl": " -e ip.ttl"
			},
			"tcp" : {
				"src": " -e tcp.srcport",
			    "dst": " -e tcp.dstport",
			    "flags": " -e tcp.flags"
			},
			"frame" : {
				"time": " -e frame.time_epoch",
				"len": " -e frame.len",
			    "num": " -e frame.number"
			},
			"udp" : {
				"src": " -e udp.srcport",
			    "dst": " -e udp.dstport"
			},
			"dns" : {
				"name": " -e dns.qry.name",
				"type": " -e dns.qry.type",
				"resp": " -e dns.a",
			    "domain": " -e dns.ptr.domain_name"
			},
			"icmp" : {
				"type": " -e icmp.type",
				"code": " -e icmp.code"
			}
		}

	def add_field(self, category, name):
		"""
		Adds field to self./fields/
		:param category: one of acceptable categories [frame, ip, tcp, icmp, dns, udp]
		:param name: name of the field available under category specified
		:return: appends selected field to /fields/
		"""
		self.fields += self.network_fields_names[category][name]

	def add_fields_by_category(self, category):
		"""
		Adds multiple fields to self./fields/ based on category
		:param category: one of acceptable categories [frame, ip, tcp, icmp, dns, udp]
		:return: appends selected fields to /fields/
		"""
		for key in self.network_fields_names[category].keys():
			self.fields +=  self.network_fields_names[category][key]

	def add_filter(self, category):
		"""
		Adds filter specifications based on selected category
		:param category:
		:return:
		"""
		if category == "tcp":
			self.filter = ' -R "(ip.proto == 6)" -2 '
		elif category == "ip":
			self.filter = ' -R "(ip.version == 4)" -2 '
		elif category == "icmp":
			self.filter = ' -R "(ip.proto == 1)" -2 '
		elif category == "udp":
			self.filter = ' -R "(ip.proto == 17)" -2 '
		elif category == "dns":
			self.filter = ' -R "(dns)" -2 '

	def create_command(self, filename, out_filename):
		"""
		Create final command
		:return:
		"""

		# Adds path to tshark executable
		self.execution_command += self.exec_path

		# Adds input directory
		self.execution_command += " -r " + self.input_path + filename

		# Adds output modifiers for CSV output
		self.execution_command += " -T fields -E header=n -E separator=, -E occurrence=f -E quote=d -t u "

		# Adds previously selected fields
		self.execution_command += self.fields

		# Adds previously selected filter
		self.execution_command += self.filter

		# Adds output directory
		self.execution_command += " > " + self.output_path + out_filename



def main():

	# Input
	test_input = "split_00000_20120316133000.pcap"

	# Output
	test_output = "test.csv"

	# Create tshark object
	shark = Tshark("tshark", "input\\", "output\\")

	# Add fields
	shark.add_fields_by_category("tcp")
	shark.add_fields_by_category("ip")

	# Add filters
	shark.add_filter("tcp")

	# Create command
	shark.create_command(test_input, test_output)

	print(shark.execution_command)

if __name__ == "__main__":
	main()