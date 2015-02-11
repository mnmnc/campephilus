import sys; import os
sys.path.insert(0, os.path.abspath('..'))

from testing import detector_lof2d_testing, netjinn_ip_testing, netjinn_tcp_testing, tshark_testing




from unittest import TestLoader, TextTestRunner, TestSuite

if __name__ == "__main__":
	# TODO: WHY THIS DOES NOT WORK?

    loader = TestLoader()
	suite = TestSuite((
        loader.loadTestsFromTestCase(netjinn_ip_testing.IPJinnTestCase.__class__),
        loader.loadTestsFromTestCase(netjinn_tcp_testing.TcpJinnTestCase.__class__),
        loader.loadTestsFromTestCase(detector_lof2d_testing.LOF2DTestCase.__class__),
        loader.loadTestsFromTestCase(tshark_testing.TsharkTestCase.__class__),
        ))

	runner = TextTestRunner(verbosity = 2)
	runner.run(suite)