

## Main file of the project

class Campephilus:

	# Common settings
	settings = {}

	def __init__(self):
		pass

	# Add dictionary element to settings
	def add_setting(self, setting):
		self.settings.update(setting)


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

	print(cam.settings)

if __name__ == "__main__":
	main()