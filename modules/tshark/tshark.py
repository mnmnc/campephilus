from subprocess import call, check_output
import os

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
			    "flags": " -e tcp.flags",
			    "seq": " -e tcp.seq",
			    "stream": " -e tcp.stream"
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

		# Initial path checks
		if not os.path.exists(self.exec_path):
			print("[ERR] Path", self.exec_path, "does not exist.")
		if not os.path.exists(self.input_path + filename):
			print("[ERR] Path", self.input_path + filename, "does not exist.")
		if not os.path.exists(self.output_path):
			print("[ERR] Path", self.output_path, "does not exist.")

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

		print(self.execution_command)

	def execute(self):
		"""
		Executes tshark /shell required/
		:return:
		"""
		try:
			call(self.execution_command, shell=True)
		except:
			print("Failed to execute tshark.")
			print("Failed command:", self.execution_command)


def main():

	# Input
	#test_input = "smaller_00002_20120316134254.pcap"
	test_input = "split_00000_20120316133000.pcap"

	# Output
	test_output = "test2.csv"

	# Create tshark object
	shark = Tshark("D:\\Apps\\Wireshark\\tshark.exe", "..\\..\\input\\pcap\\", "..\\..\\input\\csv\\")

	# Add fields
	shark.add_fields_by_category("tcp")
	shark.add_fields_by_category("ip")
	shark.add_fields_by_category("icmp")
	shark.add_fields_by_category("dns")
	shark.add_fields_by_category("frame")
	shark.add_fields_by_category("udp")


	# Add filters
	shark.add_filter("ip")

	# Create command
	shark.create_command(test_input, test_output)

	# Execute
	shark.execute()

if __name__ == "__main__":
	main()