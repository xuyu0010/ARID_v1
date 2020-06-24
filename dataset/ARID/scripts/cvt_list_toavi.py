import os

def cvt_list_toavi(dirpath):

	filenames_dict = {}

	for file in os.listdir(dirpath):
		if file == "mapping_table" or file == "avi_txt":
			continue
		else:
			old_txt = open(file, 'r')
			clip_names = old_txt.read()
			clip_names = clip_names.split('\n')
			filenames_dict[file] = clip_names
			old_txt.close()

	print("All old txt files have been loaded")

	for old_txt in filenames_dict.keys():
		new_path = os.getcwd() + "/avi_txt/" + old_txt
		print(new_path)
		new_txt = open(new_path, 'w')
		clipnames = filenames_dict[old_txt]

		for clip_name in clipnames:
			# print(clip_name)
			new_name = clip_name.replace('.mp4', '.avi')
			new_txt.write(new_name)
			new_txt.write("\n")

		print("The transformation of %s is completed." %old_txt)
		new_txt.close()

if __name__ == "__main__":
	cvt_list_toavi(os.getcwd())
    	


