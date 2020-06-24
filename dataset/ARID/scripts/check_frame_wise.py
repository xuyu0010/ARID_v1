import cv2
import numpy as np
import os

def check_frame_wise(cur_path, init_dirname, new_dirname):
	new_path = os.path.join(cur_path, new_dirname)
	pre_path = os.path.join(cur_path, init_dirname)
	for dirname in os.listdir(pre_path):
		print(dirname)
		if '.' in dirname or dirname == 'list_cvt_v1':
			continue
		init_class_path = os.path.join(pre_path, dirname)
		new_class_path = os.path.join(new_path, dirname)

		for file in os.listdir(init_class_path):
			if(os.path.splitext(file)[1] != '.avi'):
				continue
			else:
				init_clip_path = os.path.join(init_class_path, file)
				new_clip_path = os.path.join(new_class_path, file)
				cap = cv2.VideoCapture(init_clip_path)
				cap_new = cv2.VideoCapture(new_clip_path)
			if int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) == int(cap_new.get(cv2.CAP_PROP_FRAME_COUNT)):
				continue
			else:
				raise Exception("Fail to transform %s" %(file))
		print("The transformation of %s is successful" %(dirname))

if __name__ == '__main__':
	check_frame_wise(cur_path=os.getcwd(), init_dirname='clips_v1_avi', new_dirname='clips_v1_GIC_HE')

