
import sys; import os
sys.path.insert(0, os.path.abspath('..'))
from modules.netjinn import ip
import unittest

class IPJinnTestCase(unittest.TestCase):

	ip_test = ip.Ip()

	def test_string_to_decimal(self):
		"""
		Tests whether String IP conversion to decimal form is performed as expected.
		:return:
		"""
		correct = 0

		if self.ip_test.str2dec("192.168.0.1") == 3232235521:
			correct += 1
		if self.ip_test.str2dec("255.255.255.255") == 4294967295:
			correct += 1
		if self.ip_test.str2dec("255.255.255.256") == -1:
			correct += 1
		if self.ip_test.str2dec("-1.-1.-1.-1") == -1:
			correct += 1
		if self.ip_test.str2dec(".168.0.1") == -1:
			correct += 1
		if self.ip_test.str2dec("192.168.0") == -1:
			correct += 1

		self.assertEqual(correct, 6, "String IP to decimal form translation behaves incorrectly.")


if __name__ == '__main__':
	unittest.main(verbosity=2)