#!/bin/bash

# test is we are given enaough arguments

MSG="Bad number of arguments try using format <input-directory> <output-directory>"

echo Testing user input

if [ $# -eq 0 ]
then
	echo $MSG
	exit
fi

TEMP=temptemptemptemp.bed 
SOURCE=$1
OUTPUT=$2
AND=$3
COUNT=0

echo Making bed files

for i in $(ls $SOURCE/*.bam) ;
do
	bedtools bamtobed -i $i | python3 Main.py $OUTPUT $i;
	COUNT=$(($COUNT+1));
done

echo Making the unified .bed 
python3 MergeBed.py $OUTPUT $TEMP
echo Done merging
python3 Main.py $OUTPUT _unified $TEMP $AND $COUNT 
rm $TEMP
echo Done
