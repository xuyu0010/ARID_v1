#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 19:59:14 2019

@author: caohaozhi
"""

"""
Using this script ONLY under the 
"""

import os
import numpy as np
import math

# the clips of AIR are placed in the path AIR/raw/data/ and were separated 
# in different classes.

def three_splits(clips_path):
    
    class_list = []
    class_table = {}
    train_fraction = 0.7
    test_fraction = 0.3

    clip_nums = {}
    scen_nums = {}
    
    
    # Create an empty list and obtain the total classes and 
    # obtain all the path of sub directories
    for dirpath, dirnames, filenames in os.walk(clips_path):
        if dirnames != []:
            class_list = dirnames
    
    # Sorted the lists
    class_list = sorted(class_list)
        
    # Map the label with number and store the map in mapping_table.txt
    mapping_table = open('mapping_table.txt', 'w')
    
    i = 0
    for label in class_list:
        if '.' not in label and label != 'list_cvt_v1':
            class_table[i] = label
            mapping_table.write(str(i) + '\t' + label)
            mapping_table.write('\n')
            i = int(i) + 1

    mapping_table.close 

    # Construct a dict of all videos, where the indexs are classes
    paths_dict = {}
    for dirname in os.listdir(clips_path):
        if '.' in dirname or dirname == 'list_cvt_v1':
            continue
        class_path = os.path.join(clips_path, dirname)

        # Prepare the empty dict and list
        paths_dict[dirname] = {}
        clip_nums[dirname] = {}
        scen_nums[dirname] = 0
        paths_list_single = []
        paths_list = {}

        # Reset the maximum number of clips and scenarios
        max_scen_num = 1
        max_clip_nums = {}

        for file in os.listdir(class_path):
            if(os.path.splitext(file)[1] == '.mp4'):
                file_path = dirname + '/' + file
                scen_num = file.split('_')[1]
                clip_num = file.split('_')[2]
                clip_num = clip_num.split('.')[0]

                #test
                # print("filename: %s, scen_num: %s, clip_num: %s, max_scen_num: %s \n" 
                #     %(file, scen_num, clip_num, max_scen_num))

                if scen_num not in paths_list.keys():
                    paths_list[scen_num] = []
                paths_list[scen_num].append(file_path)

                if int(scen_num) > int(max_scen_num):
                    max_scen_num = scen_num

                if scen_num not in max_clip_nums.keys():
                    max_clip_nums[scen_num] = clip_num
                # print(dirname, scen_num)
                
                if int(clip_num) > int(max_clip_nums[scen_num]):
                    max_clip_nums[scen_num] = clip_num

        # paths_dict is a dict, paths_dict[action][scen] = [file_path]
        paths_dict[dirname] = paths_list
        clip_nums[dirname] = max_clip_nums
        scen_nums[dirname] = max_scen_num
                
    # The spliting rule can be seperated into two parts:
    # 1. The training and testing set are divided randomly based on different scences;
    # 2. Whether the specific clip is included into this clips is based on the randomly selection;
    #    If the total clips num in this scence is more than the average number of all scen in this action,
    #    then the clips are randomly chosen, otherwise all the clips would be included.

    # Creat train_dict and test_dict to store the clips
    shuffled_indexs = {}
    # print(clip_nums)
    # print(scen_nums)
    for i in range(3):
        shuffled_index = {}

        for action in clip_nums.keys():
            index_scen = {"train" : [], "test" : []}
            index_clip = {"train" : {}, "test" : {}, "other" : {}}

            if int(scen_nums[action]) >= 10:
                train_scen_num = math.ceil(int(scen_nums[action]) * 0.7)

                # Create a shuffled index for scences
                total_scens = np.arange(int(scen_nums[action])) + 1
                np.random.shuffle(total_scens)
                index_scen["train"] = total_scens[ : train_scen_num]
                index_scen["test"] = total_scens[train_scen_num : ]

                # Obtain the number of clips in each scens and the average number of each class
                total_clips_num = 0
                for scen in clip_nums[action].keys():
                    total_clips_num += int(clip_nums[action][scen])
                ave_clips_num = int(total_clips_num / int(scen_nums[action]))

                # Generate the shuffled_index of clips in train set and test set
                for index in ["train", "test"]:
                    for scen in index_scen[index]:
                        scen = str(scen)
                        # If clips num is less than the ave value, all clips would be involved
                        if int(clip_nums[action][scen]) <= ave_clips_num:
                            index_clip[index][scen] = list(range(int(clip_nums[action][scen])))
                        else:
                            clips_num_index = np.arange(int(clip_nums[action][scen]))
                            np.random.shuffle(clips_num_index)
                            index_clip[index][scen] = clips_num_index[0 : ave_clips_num]
                            index_clip["other"][scen] = clips_num_index[ave_clips_num : ]
                    
                # shuffled_index is a dict, shuffled_index[action][dataset][scen] = list()
                shuffled_index[action] = index_clip                 

            else:
                raise ValueError("The number of scences in %s is less than 10" %(action))

        shuffled_indexs[i] = shuffled_index

    content = []
    # Based on the shuffled_indexs, split the clips into 3 parts
    for i in range(3):   
        content.append({"train" : [], "test" : [], "other" : []})

        for key in class_table.keys():
            action = class_table[key]
            for set_index in shuffled_indexs[i][action].keys():
                path = []
                for scen in shuffled_indexs[i][action][set_index].keys() :
                    index = shuffled_indexs[i][action][set_index][scen]

                    for j in index:
                        try:
                            path.append(str(str(key) + '\t' + str(paths_dict[action][scen][j])))
                        except IndexError:
                            print(action,scen)
                            break
                
                content[i][set_index] += path


    for i in range(3):
        for index in content[i].keys():
            print_content = sorted(content[i][index])
            file = open('ARID_split' + str(i + 1) + '_' + str(index) + '.txt', 'w')
            for k in range(len(print_content)):
                file.write(str(k) + '\t' + str(print_content[k]))
                file.write('\n')           
            file.close

if __name__ == '__main__':
    clips_path = os.getcwd()
    three_splits(clips_path)
