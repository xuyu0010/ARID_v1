#!/usr/bin/env sh
# This script darkens all input video to a brightness of 0.7
# The parameters and options are found at https://ffmpeg.org/ffmpeg-filters.html#eq
cd ./dark/

for FOLDER in */; do
	echo "$FOLDER"
	mkdir ../re_bright/$FOLDER/
	cd $FOLDER/
	for FILE in *; do
		echo "$FILE"
		ffmpeg -y -loglevel fatal -i $FILE -vf eq=brightness=0.7 -c:a copy ../../re_bright/$FOLDER/$FILE
	done
	cd ../
done
echo "DONE!"
cd ../
