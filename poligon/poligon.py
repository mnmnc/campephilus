
import sys; import os
sys.path.insert(0, os.path.abspath('..'))

from modules.csvimporter import csvimp


def main():

	csv = csvimp.Csvimp("D:\\Prv\\Git\\campephilus\\input\\csv\\infinz_april_2014.csv")
	csv.load_data()
	data = []

	for packet in csv.data:
		packet_arr = packet.split(",")
		if len(packet_arr) > 2:
			tcpsrc = packet_arr[0]
			tcpdst = packet_arr[1]
			tcpflags = packet_arr[2]
			tcpstream = packet_arr[3]
			tcpseq = packet_arr[4]
			ipsrc = packet_arr[5]
			ipdst = packet_arr[6]
			ipttl = packet_arr[7]
			icmpcode = packet_arr[8]
			icmptype = packet_arr[9]
			dnsa = packet_arr[10]
			dnsqtype = packet_arr[11]
			dnsqname = packet_arr[12]
			dnsdomain = packet_arr[13]
			frameno = packet_arr[14]
			framelen = packet_arr[15]
			frametime = packet_arr[16]
			udpsrc = packet_arr[17]
			udpdst = packet_arr[18]

			data.append(
				{
					"tcpsrc": tcpsrc,
				    "tcpdst": tcpdst,
				    "tcpflags": tcpflags,
				    "tcpstream": tcpstream,
				    "tcpseq": tcpseq,
				    "ipsrc": ipsrc,
				    "ipdst": ipdst,
				    "ipttl": ipttl,
				    "icmpcode": icmpcode,
				    "icmptype": icmptype,
				    "dnsa": dnsa,
				    "dnsqtype": dnsqtype,
				    "dnsqname": dnsqname,
				    "dnsdomain": dnsdomain,
				    "frameno": frameno,
				    "framelen": framelen,
				    "frametime": frametime,
				    "udpsrc": udpsrc,
				    "udpdst": udpdst
				}
			)

	for i in range(10):
		print(data[i])


if __name__ == "__main__":
	main()