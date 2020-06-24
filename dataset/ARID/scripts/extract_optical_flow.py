import os
import numpy as np
import cv2
# import argparse
from PIL import Image
# from multiprocessing import Pool
import skvideo.io
import scipy.misc
# import imageio
import warnings
from datetime import datetime as dt

warnings.filterwarnings("ignore")
print_timespan = True

def ToImg(raw_flow,bound):
	'''
	this function scale the input pixels to 0-255 with bi-bound
	:param raw_flow: input raw pixel value (not in 0-255)
	:param bound: upper and lower bound (-bound, bound)
	:return: pixel value scale from 0 to 255
	'''
	flow=raw_flow
	flow[flow>bound]=bound
	flow[flow<-bound]=-bound
	flow-=-bound
	flow*=(255/float(2*bound))
	return flow

def save_flows(flows, save_dir, num, bound):
	'''
	To save the optical flow images and raw images
	:param flows: contains flow_x and flow_y
	:param image: raw image (Deleted)
	:param save_dir: save_dir name (always equal to the video id)
	:param num: the save id, which belongs one of the extracted frames
	:param bound: set the bi-bound to flow images
	:return: return 0
	'''
	#rescale to 0~255 with the bound setting
	flow_x=ToImg(flows[...,0],bound)
	flow_y=ToImg(flows[...,1],bound)
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)
	save_dir_x = os.path.join(save_dir, 'x')
	save_dir_y = os.path.join(save_dir, 'y')
	if not os.path.exists(save_dir_x):
		os.makedirs(save_dir_x)
	if not os.path.exists(save_dir_y):
		os.makedirs(save_dir_y)

	#save the image # In our case extract_frames.py is used
	# save_img=os.path.join(data_root,new_dir,save_dir,'img_{:05d}.jpg'.format(num))
	# scipy.misc.imsave(save_img,image)

	#save the flows
	save_x=os.path.join(save_dir_x,'flow_x_{:05d}.jpg'.format(num))
	save_y=os.path.join(save_dir_y,'flow_y_{:05d}.jpg'.format(num))
	flow_x_img=Image.fromarray(flow_x)
	flow_y_img=Image.fromarray(flow_y)
	scipy.misc.imsave(save_x,flow_x_img)
	scipy.misc.imsave(save_y,flow_y_img)
	# imageio.imwrite(save_x,flow_x_img)
	# imageio.imwrite(save_y,flow_y_img)
	return 0

def extract_of(video, save_dir, bound):
	video_name = video.split('/')[len(video.split('/'))-1]
	cap = cv2.VideoCapture(video)
	ret, frame1 = cap.read()
	prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame1)
	hsv[...,1] = 255
	i = 0
	while(1):
		ret, frame2 = cap.read()
		if ret == False:
			break
		next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
		# flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0) # Original method in tutorial
		optical_flow = cv2.optflow.createOptFlow_DualTVL1()
		flow = optical_flow.calc(prvs, next, None) # Using TV_L1 instead
		# save_flows(flow, save_dir, i, bound)

		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
		hsv[...,0] = ang*180/np.pi/2
		hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX) # Optical Flow
		bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
		save_dir_hsv = os.path.join(save_dir, 'hsv')
		if not os.path.exists(save_dir_hsv):
			os.makedirs(save_dir_hsv)
		hsvfile = os.path.join(save_dir_hsv,'flow_hsv_{:05d}.jpg'.format(i))
		cv2.imwrite(hsvfile, bgr)
		i = i+1
		prvs = next

# def get_video_list(root_dir):
# 	video_list=[]
# 	for cls_names in os.listdir(root_dir):
# 		cls_path=os.path.join(root_dir,cls_names)
# 		for video_ in os.listdir(cls_path):
# 			video_list.append(video_)
# 	video_list.sort()
# 	return video_list,len(video_list)

if __name__ == "__main__":

	cur_path = os.getcwd()
	data_root = os.path.join(cur_path, 'clips_v1')
	target_folder = 'avi'
	target_root = os.path.join(data_root, target_folder)
	of_folder = 'ori_of'
	of_path = os.path.join(data_root, of_folder)
	if not os.path.exists(of_path):
		os.mkdir(of_path)
	bound = 15
	total_files = sum([len(files) for r, d, files in os.walk(target_root)])
	video_num = 1
	# video_list, len_videos = get_video_list(target_root)

	for cls_name in os.listdir(target_root):
		if '.' in cls_name:
			continue
		cls_path = os.path.join(target_root, cls_name)
		of_cls_path = os.path.join(of_path, cls_name)
		if not os.path.exists(of_cls_path):
			os.mkdir(of_cls_path)

		for video in os.listdir(cls_path):
			if(os.path.splitext(video)[1] != '.avi'):
				continue
			print("Processing {}".format(video))
			begin = dt.now()
			video_path = os.path.join(cls_path, video)
			video_of_path = os.path.join(of_cls_path, video)
			if not os.path.exists(video_of_path):
				os.mkdir(video_of_path)
			extract_of(video_path, video_of_path, bound)
			end = dt.now()
			print("Process {} completed ({}/{})".format(video, video_num, total_files))
			if print_timespan:
				span = (end - begin).total_seconds()
				print("One video takes {} seconds to convert".format(span))
			video_num += 1