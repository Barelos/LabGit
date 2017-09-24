#!/bin/bash

# CONSTANTS
MSG="Given a folder with BAM files find windows around the TTS.\nFormat: sh main.sh <input folder>"

if [ $# -eq 0 ]
then
	echo $MSG
	exit
fi

FOLDER=$1 # the working directory
JUMP=20 # how close must to windows be to be merged
files=($FOLDER/*.bam)
BAM_COUNT=${#files[@]} # num of input BAM files
GLOBAL_FILENAME=global_windows.bed # name of output file

# make BED files of local windows and save them in FOLDER
./make_bed.sh $FOLDER $JUMP # change back to make_bed.sh

# make global windows and remove
./make_global.sh $FOLDER $GLOBAL_FILENAME

# on the global window file delete "noise" windows and collect fetures for future analysis
python3 window_sort.py $FOLDER $GLOBAL_FILENAME $BAM_COUNT
