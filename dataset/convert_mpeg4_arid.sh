#!/usr/bin/env sh
# This script copies the files to the designated folder

cd /data/AID11/clips_v1/mpeg4
mkdir /data/AID11/clips_v1/avi/

for FOLDER in */; do
	echo "$FOLDER"
	mkdir /data/AID11/clips_v1/avi/$FOLDER/
	cd $FOLDER/
	for FILE in *; do
		echo "$FILE"
		FILENAME=$(echo "$FILE" | cut -f 1 -d '.')
		echo "$FILENAME"
		ffmpeg -loglevel error -y -i $FILE -c:v mpeg4 -filter:v "scale=min(iw\,(256*iw)/min(iw\,ih)):-1" -b:v 512k -an $FILENAME.avi
	done
	mv *.avi /data/AID11/clips_v1/avi/$FOLDER/
	cd ../
	echo "Transformed to AVI files and moved to designated folder"

done
