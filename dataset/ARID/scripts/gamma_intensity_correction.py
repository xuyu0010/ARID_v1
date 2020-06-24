import cv2
import numpy as np
import os

def adjust_gamma_table(gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return table

def gamma_intensity_correction(cur_path, init_dirname, gamma):

	os.mkdir('gamma_correction')
	new_path = os.path.join(cur_path, 'gamma_correction')
	LU_table = adjust_gamma_table(gamma)
	for name in os.listdir(cur_path):
		if name != init_dirname:
			continue
		else:
			init_path = os.path.join(cur_path, name)

		for dirname in os.listdir(init_path):
			print(dirname)
			if '.' in dirname or dirname == 'list_cvt_v1':
				continue
			class_path = os.path.join(init_path, dirname)
			dirpath = os.path.join(new_path, dirname)
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

				while(True):
					ret, frame = cap.read()
					if ret == True:
						new_frame = cv2.LUT(frame, LU_table)
						# cv2.imshow("New Frame", new_frame)
						# cv2.waitKey(int(fps))
						cap_writer.write(new_frame)
					else:
						print("Completed the processing of %s" %(file))
						break

				cv2.destroyAllWindows()     # close all the widows opened inside the program
				cap.release        			# release the video read/write handler
				cap_writer.release
				# cap_new = cv2.VideoCapture(os.path.join(dirpath,file))
				# length_new = int(cap_new.get(cv2.CAP_PROP_FRAME_COUNT))

				# if length_new == length_pre:
				# 	print("Completed the processing of %s" %(file))
				# else:
				# 	print("length_new:%d, length_pre:%d" %(length_new, length_pre))
				# 	raise Exception("Fail to transform %s" %(file))

				# cap_new.release        			# release the video read/write handler

if __name__ == '__main__':
	gamma_intensity_correction(os.getcwd(), init_dirname='avi', gamma=10)
