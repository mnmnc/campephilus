## Main file of the project

from modules.tshark import tshark

class Campephilus:

	# Common settings
	settings = {}
	tools = {}

	def __init__(self):
		pass

	# Add dictionary element to settings
	def add_setting(self, setting):
		self.settings.update(setting)

	def add_tool(self, tool):
		self.tools.update(tool)

	def showoff(self, values = False):
		sorted(self.settings, key=lambda k: len(self.settings[k]))
		print(self.settings)

		if values == False:
			for key in self.settings.keys():
				print("settings."+key)
			for key in self.tools.keys():
				print("tools."+key)
		else:
			for key in self.settings.keys():
				print("settings."+key, "\t", str(self.settings[key]))
			for key in self.tools.keys():
				print("tools."+key, "\t", str(self.tools[key]))

def main():

	cam = Campephilus()
	cam.add_setting({"input":"input\\"})
	cam.add_setting({"output":"output\\"})
	cam.add_setting({"tshark":"D:\\Apps\\Wireshark\\tshark.exe"})
	cam.add_setting({"pcap_files":"pcap\\"})
	cam.add_setting({"csv_files":"csv\\"})
	cam.add_setting({"csv_file_name":"campephilus"})
	cam.add_setting({"png_file_name":"campephilus"})
	cam.add_setting({"animated_file":"campephilus"})

	# Create Thark (exe, in , out)  object
	shark = tshark.Tshark(
				cam.settings["tshark"],
				cam.settings["input"] +	cam.settings["pcap_files"],
				cam.settings["output"] + cam.settings["csv_files"])

	# Add fields
	shark.add_fields_by_category("ip")

	# Add limitation filter
	shark.add_filter("ip")

	# Create command
	shark.create_command("losowe.pcap", "out.csv")

	# Add to tolls
	cam.add_tool({"shark":shark})



	# Show me what you got
	cam.showoff(True)

if __name__ == "__main__":
	main()