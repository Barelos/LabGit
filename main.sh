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
