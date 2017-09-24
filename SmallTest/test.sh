#!/bin/bash

# input
FOLDER="SmallTest" # the working directory
JUMP=$2 # how close must two reads be

# constants
OUTPUT="final.bed"
EXTENSION=".bed"

# iterate through the BAM files and turn them into window files
for i in $(ls *.bed); do
	x=${i%.bed} # make the file name
	# make the gonomecov file and sort it by chromosome and starting base
	awk '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $4, $4 * ($3 - $2), "+")}' $i > new_$x$EXTENSION
	sort -k 1,1 -k2,2n new_$x$EXTENSION > ${x}_sorted$EXTENSION # this file is a graph like representation of a bed file
	bedtools merge -s -d $JUMP -c 5 -o sum -i ${x}_sorted$EXTENSION | awk -v var="$x" '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, var, $5, $4)}' >> $OUTPUT
done

# sort the global file in order to use merge on it
sort -k 1,1 -k2,2n $OUTPUT > sorted_$OUTPUT # before merge
bedtools merge -s -c 5 -o sum -i sorted_$OUTPUT | awk '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $3 - $2, $4, $4)}' > $OUTPUT # this are the global windows sorted by chromosome and starting base

echo "Done making BED files"