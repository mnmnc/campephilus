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
	#cam.tools["shark"].add_field("frame", "time")
	cam.tools["shark"].add_field("tcp", "stream")
	cam.tools["shark"].add_field("tcp", "seq")
	#cam.tools["shark"].add_field("tcp", "flags")
	cam.tools["shark"].add_field("tcp", "src")
	cam.tools["shark"].add_field("tcp", "dst")

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

	for row in cam.jobs["job_id"]["data"]:
		print(row)

	t = cam.tools["tcp"].split_data_to_streams(cam.jobs["job_id"]["data"], 0)

	for row in t:
		print(row, ":")
		for packet in t[row]:
			print("\t",packet)
	# 	name = "D:\\OUT4\\stream_" + row + ".png"
	# 	xs = []
	# 	ys = []
	# 	for packet in t[row]:
	# 		print("\t",packet)
	# 		xs.append(packet[0])
	# 		ys.append(packet[1])
	# 		xs.append(packet[0])
	# 		ys.append(packet[2])
	#
	# 	cam.tools["plot"].plot( xs,ys , "line", "b", 0.7)
	# 	cam.tools["plot"].save(name)
	# 	cam.tools["plot"].clear_plot()
	#
	#
	# cam.tools["plot"].plot([1,4,9,16], [1,2,3,4], "line", "r", 0.4)
	# cam.tools["plot"].save("D:\\test.png")



if __name__ == "__main__":
	main()