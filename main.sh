#!/bin/bash

# CONSTANTS
MSG="Given a folder with BAM files find windows around the TTS.\nFormat: sh main.sh <input folder>"
SCRIPTS="make_bedtools.sh make_features.sh"
if [ $# -eq 0 ]
then
	echo $MSG
	exit
fi

FOLDER=$1 # the working directory
JUMP=20 # how close must to windows be to be merged

# make sure we can run all our files
chmod 777 $SCRIPTS

# makes the global window and local graph like file for each BAM file
./make_bedtools.sh $FOLDER $JUMP

# make a global file and a local file for each original BAM file with features
./make_features.sh