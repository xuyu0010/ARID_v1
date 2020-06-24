import os 
import logging

def split_test_class():
	test_split = {}
	print("Begin to split the test clips")
	for dirpath, dirnames, filenames in os.walk(os.getcwd()):
		if filenames != []:
			for filename in filenames:
				if "test.txt" in filename:
					test_split[filename.split('_')[1]] = {}
	logging.info("Here is total split: {}".format(test_split.keys()))

	for split in test_split.keys():
		test_txt = "ARID_" + str(split) + "_test.txt"
		txt_path = os.path.join(os.getcwd(), test_txt)
		assert os.path.exists(txt_path)
		f = open(txt_path, 'r')
		clip_dict = {"0": []}
		prev_class_num = 0

		for clip in f.readlines():
			class_num = clip.split('\t')[1]
			clip_path = clip.split('\t')[2]
			if class_num == prev_class_num:
				clip_dict[class_num].append(clip_path)
			else:
				clip_dict[class_num] = [clip_path]
				prev_class_num = class_num

		for num in clip_dict.keys():
			clips_per_class = clip_dict[num]
			filename = 'ARID_' + str(split) + '_test_' + str(num) + '.txt'
			file = open(filename, 'w')
			for i in range(len(clips_per_class)):
				file.write(str(i) + '\t' + str(num) + '\t' + str(clips_per_class[i]))
				if i == (len(clips_per_class)-1):
					
			file.close()
			logging.info("Complete writing {}".format(filename))


if __name__ == '__main__':
	split_test_class()





