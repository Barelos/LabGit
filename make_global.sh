#!/bin/bash

FOLDER=$1 # the working directory
NAME=$2

# create intersect file w.r.t strand save all the data of the intersected windows
files=($FOLDER/*.bed)
bedtools intersect -a ${files[0]} -b ${files[@]:1} -wo -s > $FOLDER/$NAME
# rm ${files[@]}
echo "Done making global windows"
