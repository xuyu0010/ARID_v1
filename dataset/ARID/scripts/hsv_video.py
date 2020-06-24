import os
import cv2
from datetime import datetime as dt

total = 3784
i = 1
fps = 30
size = (320, 240)
print_timespan = True


cur_path = os.getcwd()
data_root = os.path.join(cur_path, 'clips_v1')
target_folder = 'ori_of'
target_root = os.path.join(data_root, target_folder)
dest_folder = 'hsv_avi'
dest_root = os.path.join(data_root, dest_folder)
if not os.path.exists(dest_root):
	os.mkdir(dest_root)

for cls_name in os.listdir(target_root):

	cls_folder = os.path.join(target_root, cls_name)
	dest_cls_folder = os.path.join(dest_root, cls_name)
	if not os.path.exists(dest_cls_folder):
		os.mkdir(dest_cls_folder)

	for video in os.listdir(cls_folder):
		print('Processing video {} ({}/{})'.format(video, i, total))
		begin = dt.now()

		video_hsv_folder = os.path.join(cls_folder, video, 'hsv')
		dest_hsv_avi = os.path.join(dest_cls_folder, video)
		cap_writer = cv2.VideoWriter(dest_hsv_avi, cv2.VideoWriter_fourcc('X', '2', '6', '4'), fps, size)

		for hsv_frame in sorted(os.listdir(video_hsv_folder)):
			hsv_frame_path = os.path.join(video_hsv_folder, hsv_frame)
			cap_writer.write(cv2.imread(hsv_frame_path))

		cv2.destroyAllWindows()     # close all the widows opened inside the program
		cap_writer.release
		end = dt.now()
		i += 1
		if print_timespan:
			span = (end - begin).total_seconds()
			print("One video takes {} seconds to convert".format(span))