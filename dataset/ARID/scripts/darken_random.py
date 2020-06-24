import os
import sys
import glob
import numpy as np
import scipy as sp
import subprocess

target_folder = 'rand_dark'
root_folder = 'test'
i = 1
total_files = sum([len(files) for r, d, files in os.walk(root_folder)])

if not os.path.exists(target_folder):
	os.mkdir(target_folder)

for dir in os.listdir(root_folder):
	class_folder = os.path.join(root_folder, dir)
	target_class_folder = os.path.join(target_folder, dir)
	if not os.path.exists(target_class_folder):
		os.mkdir(target_class_folder)
	files = glob.glob(os.path.join(class_folder, '*.avi'))
	for file in files:
		print("Processing {}".format(file))
		filename = file.split('/')[-1]
		output_file = os.path.join(target_class_folder, filename)
		mean, std = 0.2, 0.07
		gam_val = np.random.normal(mean, std)
		if gam_val <= 0.1:
			gam_val = 0.1
		eq_filter = 'eq=gamma={}'.format(str(gam_val))
		subprocess.call(['ffmpeg', '-y', '-loglevel', 'fatal', '-i', file, 
						'-vf', eq_filter, '-c:a', 'copy', output_file])
		print("Process {} completed ({}/{})".format(file, i, total_files))
		i = i + 1
