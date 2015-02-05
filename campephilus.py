# Main file of the project

from modules.tshark import tshark
from modules.csvimporter import csvimp
from modules.netjinn import tcp
from modules.netjinn import ip
from modules.plotter import plot

class Campephilus:

	# Common settings
	settings = {}
	tools = {}
	jobs = {}

	def __init__(self):
		pass

	# Add dictionary element to settings
	def add_setting(self, setting):
		"""
		Adds setting element.
		:param setting: dictionary element expected.
		:return:
		"""
		self.settings.update(setting)

	def add_tool(self, tool):
		"""
		Adds tools to self./tools/
		:param tool: dictionary element expected.
		:return:
		"""
		self.tools.update(tool)

	def showoff(self, values=False):
		"""
		Showing settings and tools content.
		:param values: Whether to show inner values or not
		:return:
		"""

		# Sorting keys for prettier printing
		sorted_list = sorted(self.settings, key=lambda k: len(k))

		if values:
			for i in range(len(sorted_list)):
				print("settings." + sorted_list[i], "\t", str(self.settings[sorted_list[i]]))
			for key in self.tools.keys():
				print("tools." + key, "\t", str(self.tools[key]))
		else:
			for i in range(len(sorted_list)):
				print("settings." + sorted_list[i])
			for key in self.tools.keys():
				print("tools." + key)

	def get_headers(self, headers_string):
		"""
		Reads headers names from tshark fields string.
		For example
			['ip.src', 'ip.dst', 'ip.ttl'] from
			" -e ip.src -e ip.dst -e ip.ttl "

		:param headers_string:
		:return:
		"""
		headers = []
		tmp = headers_string.split("-e")
		for item in tmp:
			trimmed = item.strip(" ")
			if len(trimmed) > 0:
				headers.append(trimmed)
		return headers


def numeric_compare(x, y):
	return x - y

def main():

	cam = Campephilus()

	# Settings
	cam.add_setting({"input": "D:\\Prv\\Git\\campephilus\\input\\"})
	cam.add_setting({"output": "D:\\Prv\\Git\\campephilus\\output\\"})
	cam.add_setting({"tshark": "D:\\Apps\\Wireshark\\tshark.exe"})
	cam.add_setting({"pcap_files": "pcap\\"})
	cam.add_setting({"csv_files": "csv\\"})
	cam.add_setting({"csv_file_name": "campephilus"})
	cam.add_setting({"png_file_name": "campephilus"})
	cam.add_setting({"animated_file": "campephilus"})

	# Add tools

	# CSV tool for parsing csv files to lists
	cam.add_tool({"csv":
		csvimp.Csvimp(
			cam.settings["input"] +
			cam.settings["csv_files"] +
			"out.csv"
		)
	})

	# Create Thark (exe, in , out) object
	cam.add_tool({"shark":
		tshark.Tshark(
			cam.settings["tshark"],
			cam.settings["input"] + cam.settings["pcap_files"],
			cam.settings["input"] + cam.settings["csv_files"]
		)
	})

	cam.add_tool({"plot":plot.Plot()})
	plot.plt.gcf()


	# Create TCP and IP tools
	cam.add_tool({"tcp": tcp.Tcp()})
	cam.add_tool({"ip": ip.Ip()})

	# Add fields
	# cam.tools["shark"].add_field("frame", "time")
	# cam.tools["shark"].add_field("tcp", "stream")
	# cam.tools["shark"].add_field("tcp", "seq")
	# cam.tools["shark"].add_field("tcp", "flags")
	# cam.tools["shark"].add_field("tcp", "src")
	# cam.tools["shark"].add_field("tcp", "dst")
	#cam.tools["shark"].add_fields_by_category("frame")
	# cam.tools["shark"].add_fields_by_category("ip")
	# cam.tools["shark"].add_fields_by_category("tcp")
	cam.tools["shark"].add_field("ip", "src")
	cam.tools["shark"].add_field("ip", "dst")
	cam.tools["shark"].add_field("tcp", "stream")
	cam.tools["shark"].add_field("tcp", "flags")

	# Add limitation filter
	cam.tools["shark"].add_filter("tcp")

	# Create command
	cam.tools["shark"].create_command("infinz_00001_20140408174617.pcap", "out.csv")

	# Show me what you got
	#cam.showoff(True)

	# Execute shark
	cam.tools["shark"].execute()

	# Load data from csv file
	cam.tools["csv"].load_data()

	# Update jobs with data
	cam.jobs.update({
		"job_id": {
			"headers": cam.get_headers(cam.tools["shark"].fields),
			"data": cam.tools["csv"].data
		}
	})


	###
	### TESTING
	###

	# List of IP pairs (unique pairs so A:B equals B:A)
	ip_list = []

	# List of streams per given IP address pair
	stream_dictionary = {}

	# List of flags per stream
	# FIN SYN RST PSH ACK URG ECN CWR NCE RSD
	flags_dictionary = {}

	# Collecting IP address pairs
	for row in cam.jobs["job_id"]["data"]:
		if {row[0], row[1]} in ip_list:
			pass
		else:
			ip_list.append({row[0], row[1]})

	# Collecting stream IDs for given IP address pair
	for i in range(len(ip_list)):
		stream_inner_dictionary = []
		for row in cam.jobs["job_id"]["data"]:
			if {row[0], row[1]} == ip_list[i]:
				if row[2] not in stream_inner_dictionary:
					stream_inner_dictionary.append(row[2])
		stream_dictionary.update({i:stream_inner_dictionary})

	# Collecting flags count per stream per IP address pair
	for key in stream_dictionary.keys():
		for stream in stream_dictionary[key]:
			flags = [0,0,0,0,0,0,0,0,0,0,0,0]
			for row in cam.jobs["job_id"]["data"]:
				if {row[0], row[1]} == ip_list[key] and row[2] == stream:
					flags_dict = cam.tools["tcp"].flags_to_string_list(row[3])
					if flags_dict["fin"] == 1:
						flags[0] += 1
					if flags_dict["syn"] == 1:
						flags[1] += 1
					if flags_dict["rst"] == 1:
						flags[2] += 1
					if flags_dict["psh"] == 1:
						flags[3] += 1
					if flags_dict["ack"] == 1:
						flags[4] += 1
					if flags_dict["urg"] == 1:
						flags[5] += 1
					if flags_dict["ecn"] == 1:
						flags[6] += 1
					if flags_dict["cwr"] == 1:
						flags[7] += 1
					if flags_dict["nce"] == 1:
						flags[8] += 1
					if flags_dict["rsvd1"] == 1 or flags_dict["rsvd2"] == 1 or flags_dict["rsvd3"] == 1 :
						flags[9] += 1
			flags_dictionary.update({stream: flags})

	# Printing results:
	# 0
	# 	 0 {'87.205.141.29', '37.187.81.8'} [2, 0, 0, 30, 49, 0, 0, 0, 0, 0, 0, 0]
	# 1
	# 	 1 {'198.13.112.236', '37.187.81.8'} [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
	# 2
	# 	 2 {'5.135.250.51', '37.187.81.8'} [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
	# 	 3 {'5.135.250.51', '37.187.81.8'} [0, 2, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0]

	for key in stream_dictionary.keys():
	#print(key)
		for stream in stream_dictionary[key]:
			print("\t", stream, ip_list[key], flags_dictionary[stream])





if __name__ == "__main__":
	main()