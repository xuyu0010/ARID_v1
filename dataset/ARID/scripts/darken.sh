#!/usr/bin/env sh
# This script darkens all input video to a brightness of -0.7
# The parameters and options are found at https://ffmpeg.org/ffmpeg-filters.html#eq
cd ./data/

for FOLDER in */; do
	echo "$FOLDER"
	mkdir ../dark/$FOLDER/
	cd $FOLDER/
	for FILE in *; do
		echo "$FILE"
		# ffmpeg -y -loglevel fatal -i $FILE -vf eq=brightness=-0.7 -c:a copy ../../dark/$FOLDER/$FILE
		ffmpeg -y -loglevel fatal -i $FILE -vf eq=gamma=0.5 -c:a copy ../../dark/$FOLDER/$FILE
	done
	cd ../
done
echo "DONE!"
cd ../
