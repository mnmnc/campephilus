import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from modules.tshark import tshark
from modules.csvimporter import csvimp
from modules.netjinn import tcp
from modules.netjinn import ip
from modules.plotter import plot
from modules.detector import lof2d
import campephilus
import pydoc
from io import StringIO  # Python3


def get_documentation(module):
	old_stdout = sys.stdout
	result = StringIO()
	sys.stdout = result

	help(module)

	sys.stdout = old_stdout
	result_string = result.getvalue()

	return result_string

def main():

	modules = [
		(tshark, "tshark"),
		(csvimp, "csvimp"),
		(tcp, "tcp"),
		(ip, "ip"),
		(plot, "plot"),
		(lof2d, "lof2d"),
		(campephilus, "campephilus")
	]

	full_doc = ""
	for m in modules:
		with open("D:\\Prv\\Git\\campephilus\\documentation\\" + m[1] + ".txt", "w") as file:
			module_doc = get_documentation(m[0])
			file.write(module_doc)
			full_doc += module_doc

	with open("D:\\Prv\\Git\\campephilus\\documentation.txt", "w") as file:
		file.write(full_doc)

if __name__ == "__main__":
	main()