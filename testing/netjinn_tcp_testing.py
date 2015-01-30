import sys; import os
sys.path.insert(0, os.path.abspath('..'))
from modules.netjinn import tcp
import unittest

class TcpJinnTestCase(unittest.TestCase):

	tcp_test = tcp.Tcp()



	def test_flag_translation(self):
		"""
		Tests if below translation is correct:
			2048  - RESERVED
			1024  - RESERVED
			512   - RESERVED
			256   - NONCE
			128   - CONGESTION WINDOW REDUCED
			64    - ECN-ECHO
			32    - URG
			16    - ACK
			8     - PUSH
			4     - RST
			2     - SYN
			1     - FIN
		:return: passes assertion
		"""

		correct = 0
		if (self.tcp_test.flags_to_string_list(1))["fin"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(2))["syn"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(4))["rst"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(8))["psh"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(16))["ack"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(32))["urg"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(64))["ecn"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(128))["cwr"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(256))["nce"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(512))["rsvd1"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(1024))["rsvd2"] == 1:
			correct += 1
		if (self.tcp_test.flags_to_string_list(2048))["rsvd3"] == 1:
			correct += 1

		self.assertEqual(correct, 12)


if __name__ == '__main__':
	unittest.main(verbosity=2)