import numpy as np
import copy
from matplotlib import pyplot as plt
from afmprocessing.imagedata.jpktxtfile import create_height_image

def remove_scars(datafield, threshold=0.5, show_figure=False):
	"""
	Remove scanning artifacts (scars) from AFM height data.
	
	Parameters:
		data (np.ndarray): 2D array of height data
		threshold (float): Threshold value for scar detection (default: 0.5)
	"""
	prev_rows = datafield[:-2]  # rows above
	curr_rows = datafield[1:-1]  # current rows
	next_rows = datafield[2:]   # rows below
	
	mask = np.abs(prev_rows - next_rows) < threshold * np.abs(curr_rows - next_rows)
	
	result = copy.deepcopy(datafield)
	result[1:-1][mask] = prev_rows[mask]

	if show_figure:
		fig, axarr = plt.subplots(nrows=1, ncols=2, figsize=(15, 6), tight_layout=True)
		axarr = axarr.reshape(1, 2)  # Reshape to 2D array
		axarr[0,0].imshow(create_height_image(datafield), cmap='gray')
		axarr[0,0].set_title("Input image")
		axarr[0,1].imshow(create_height_image(result), cmap='gray')
		axarr[0,1].set_title("Image after removing scars")

		for ax in axarr.ravel():
			ax.set_axis_off()

		plt.tight_layout()
		plt.show()
	
	return result

def zero_min_value(datafield):
	"""
	Shift the values so that the minimum value becomes zero.
	"""
	min_value = np.min(datafield)
	datafield_cp = copy.deepcopy(datafield)

	return datafield_cp - min_value