import inspect

class Ip:
	def __init__(self):
		pass

	def str2dec(self, ip_string):
		"""Convert IP from dot octet notation to single decimal"""
		ip_arr = ip_string.split(".")
		if len(ip_arr) == 4:
			for octet in ip_arr:
				if len(octet.strip(" ")) > 0:
					result = int(ip_arr[0]) * 256 * 256 * 256 + \
					       int(ip_arr[1]) * 256 * 256 + \
					       int(ip_arr[2]) * 256 + \
					       int(ip_arr[3])
					if result > 4294967295 or result < 0:
						print("[ERR] IP out of IPv4 range detected.", ip_string)
						return -1
					else:
						return result

				else:
					print("[ERR] Missing octets detected.", ip_string)
					return -1
		else:
			print("[ERR] Provided IP", ip_string, "does not contain 4 octets.")
			return -1


def main():

	ip = Ip()
	print(ip.str2dec("192.168.0.1"))
	print(ip.str2dec("255.255.255.255"))
	print(ip.str2dec("255.255.255.256"))
	print(ip.str2dec(" .168.0.1"))

if __name__ == "__main__":
	main()