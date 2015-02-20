
import sys; import os
sys.path.insert(0, os.path.abspath('..'))

from modules.csvimporter import csvimp
from modules.plotter import plot

def main():

	csv = csvimp.Csvimp("D:\\Prv\\Git\\campephilus\\input\\csv\\infinz_april_2014.csv")
	csv.load_data()
	data = []

	for packet_arr in csv.data:
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

	plt = plot.Plot()


	rst = {}
	syn = {}

	for ele in data:
		date = float(ele["frametime"])
		hour = int(date / 3600)

		if ele["tcpflags"] == "2":
			# SYN
			if hour in syn.keys():
				syn[hour] += 1
			else:
				syn.update({hour: 1})
		elif ele["tcpflags"] == "16":
			# RST
			if hour in rst.keys():
				rst[hour] += 1
			else:
				rst.update({hour: 1})

	xs = []
	ys = []

	for key in rst.keys():
		r = 0
		s = 0
		try:
			r = rst[key]
		except:
			r = 0

		try:
			s = syn[key]
		except:
			s = 0

		xs.append(key)
		if s > 0:
			ys.append( r / s )
		else:
			ys.append( 0 )

	plt.plot(xs, ys, "circle", "r", 0.4)





	plt.save("ack_syn_flags_ratio_per_hour3.png", 30, 8, 300)


if __name__ == "__main__":
	main()