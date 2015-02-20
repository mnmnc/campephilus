
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
		elif ele["tcpflags"] == "4" or ele["tcpflags"] == "14":
			# RST
			if hour in rst.keys():
				rst[hour] += 1
			else:
				rst.update({hour: 1})

	xs = []
	ys = []

	for key in rst.keys():
		xs.append(key)
		ys.append(rst[key])

	plt.plot(xs, ys, "circle", "r", 0.4)

	xss = []
	yss = []

	for key in syn.keys():
		xss.append(key)
		yss.append(syn[key])

	plt.plot(xss, yss, "circle", "b", 0.4)



	plt.save("syn_rst_flags_per_hour.png", 30, 8)


if __name__ == "__main__":
	main()