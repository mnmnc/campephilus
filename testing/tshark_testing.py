import sys; import os
sys.path.insert(0, os.path.abspath('..'))

from modules.tshark import tshark

import unittest

class TsharkTestCase(unittest.TestCase):

	shark = tshark.Tshark("tshark", "input\\", "output\\")

	def test_tshark_exec_path___(self):
		test_input = "split_00000_20120316133000.pcap"
		test_output = "test.csv"
		self.shark.add_filter("tcp")
		self.shark.create_command(test_input, test_output)
		self.assertTrue(len(self.shark.execution_command) > 10)

	def test_tshark_tcp_fields__(self):
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark.add_fields_by_category("tcp")
		self.assertEqual( self.shark.fields.count("tcp") , 5)

	def test_tshark_ip_fields___(self):
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark.add_fields_by_category("ip")
		self.assertEqual( self.shark.fields.count("ip") , 3)

	def test_tshark_icmp_fields_(self):
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark.add_fields_by_category("icmp")
		self.assertEqual( self.shark.fields.count("icmp") , 2)

	def test_tshark_dns_fields__(self):
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark.add_fields_by_category("dns")
		self.assertEqual( self.shark.fields.count("dns") , 4)

	def test_tshark_frame_fields(self):
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark.add_fields_by_category("frame")
		self.assertEqual( self.shark.fields.count("frame") , 3)

	def test_tshark_udp_fields__(self):
		self.shark = tshark.Tshark("tshark", "input\\", "output\\")
		self.shark.add_fields_by_category("udp")
		self.assertEqual( self.shark.fields.count("udp") , 2)

if __name__ == '__main__':

	unittest.main(verbosity=2)