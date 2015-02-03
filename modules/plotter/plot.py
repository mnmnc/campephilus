import matplotlib.pyplot as plt

class Plot:

	def save(self, destination_filename="plotted.png", width=10, height=10, local_dpi=100):
		fig = plt.gcf()
		fig.set_size_inches(width, height)
		plt.savefig(destination_filename, dpi=local_dpi)

	def plot(self, xlist, ylist, marker_style='circle', def_color="r", def_alpha=0.5, mylinewidth=2.0):
		if marker_style == "circle":
			plt.plot(xlist, ylist, def_color+'o', alpha=def_alpha)
		elif marker_style == "pixel":
			plt.plot(xlist, ylist, def_color+',', alpha=def_alpha)
		elif marker_style == "point":
			plt.plot(xlist, ylist, def_color+'.', alpha=def_alpha)
		elif marker_style == "x":
			plt.plot(xlist, ylist, def_color+'x', alpha=def_alpha)
		elif marker_style == "line":
			plt.plot(xlist, ylist, def_color+'-', alpha=def_alpha, linewidth=mylinewidth)
		elif marker_style == "triangle":
			plt.plot(xlist, ylist, def_color+'^', alpha=def_alpha)
		else:
			plt.plot(xlist, ylist, def_color+'o', alpha=def_alpha)


	def plot_with_sizes(self, xlist, ylist, sizes, marker_style='circle', def_color="r", def_alpha=0.5):
		if marker_style == "circle":
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)
		elif marker_style == "pixel":
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)
		elif marker_style == "point":
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)
		elif marker_style == "x":
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)
		elif marker_style == "line":
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)
		elif marker_style == "triangle":
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)
		else:
			plt.scatter(xlist, ylist, s=sizes, alpha=def_alpha)


	def set_label(self, axis_name, label):
		if axis_name == "x":
			plt.xlabel(label)
		elif axis_name == "y":
			plt.ylabel(label)
		else:
			print("[ERR] Unknown label", label)


	def set_title(self, title="Title", size=12):
		font = {'fontname':'Courier New','fontsize':size}
		plt.title(title, **font)

	def set_text(self, x=0, y=0, text="Text missing"):
		plt.text(x, y, text)


	def set_axis_limit(self, min_x=0, max_x=100, min_y=0, max_y=100):
		plt.axis([min_x, max_x, min_y, max_y])


	def set_note(self, x,y, text_x, text_y, text):
		"""
		x,y - pointed end
		text_x, text_y - location of the text
		"""
		plt.annotate(text, xy=(x, y),
					xytext=(text_x, text_y),
					arrowprops=dict(
						facecolor='black',
						shrink=0.08,
						width=1.0,
						headwidth=5.0,
						alpha=0.3
					)
		)


	def clear_plot(self):
		plt.clf()


def main():
	out_image = "D:\\out.png"
	pl = Plot()
	#plt.plot([1,2,3,4], [1,4,9,16], 'ro')
	pl.set_axis_limit(10,10)
	pl.plot([1,4,9,16], [1,2,3,4], "line", "b", 0.4)

	#plot([8,4,9,16], [11,14,3,4], 'y^', ms=8.0, alpha=0.4)

	f = plt.gcf()


	pl.save(out_image)


	pass

if __name__ == "__main__":
	main()