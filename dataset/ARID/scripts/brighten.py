import cv2
import numpy as np
import os
import warnings
from datetime import datetime as dt

# from ying import Ying_2017_CAIP
from LIME import LIME as lime
# from simplyLIME import simplyLIME as lime
# from dhe import dhe

warnings.filterwarnings("ignore")

def adjust_gamma_table(gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return table

def brighten(cur_path, init_dirname, is_gamma=True, method='Ying_CAIP', gamma=1.0, print_timespan=False):

	method_path = method

	if not os.path.exists(method_path):
		os.mkdir(method_path)
	new_path = os.path.join(cur_path, method_path)

	if is_gamma:
		transform = adjust_gamma_table(gamma)
	else:
		gamma = 1.0

	for name in os.listdir(cur_path):
		if name != init_dirname:
			continue
		else:
			init_path = os.path.join(cur_path, name)

		for dirname in os.listdir(init_path):
			print(dirname)
			print("Start time: {}".format(dt.now()))
			if '.' in dirname or dirname == 'list_cvt_v1':
				continue
			class_path = os.path.join(init_path, dirname)
			dirpath = os.path.join(new_path, dirname)
			if not os.path.exists(dirpath):
				os.mkdir(dirpath)

			for file in os.listdir(class_path):
				if(os.path.splitext(file)[1] != '.avi'):
					continue
				# capture the video frame by frame
				clip_path = os.path.join(class_path, file)
				cap = cv2.VideoCapture(clip_path)
				length_pre = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
				fps = cap.get(cv2.CAP_PROP_FPS)
				size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
						int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
				cap_writer = cv2.VideoWriter(os.path.join(dirpath,file), cv2.VideoWriter_fourcc('X', '2', '6', '4'), fps, size)

				begin = dt.now()
				while(True):
					ret, frame = cap.read()
					
					if ret == True:
						if is_gamma or method.upper() == 'GAMMA':
							new_frame = cv2.LUT(frame, LU_table)
						else:
							if method.upper() == 'YING_CAIP':
								new_frame = Ying_2017_CAIP(frame)
							elif method.upper() == 'DHE':
								new_frame = dhe(frame)
							elif method.upper() == 'LIME':
								new_frame = lime(frame, print_process=False)
								new_frame = new_frame.enhance()
						cap_writer.write(new_frame)
					
					else:
						print("Completed the processing of %s" %(file))
						end = dt.now()
						if print_timespan:
							span = (end - begin).total_seconds()
							print("One video takes {} seconds to convert".format(span))
						break

				cv2.destroyAllWindows()     # close all the widows opened inside the program
				cap.release        			# release the video read/write handler
				cap_writer.release


			print("End time: {}".format(dt.now()))

if __name__ == '__main__':
	brighten(os.getcwd(), init_dirname='test', is_gamma=False, method='lime', print_timespan=True)
