#!/bin/bash

# input
FOLDER=$1 # the working directory
JUMP=$2 # how close must two reads be

# constants
OUTPUT="final.bed"
EXTENSION=".bed"

# iterate through the BAM files and turn them into window files
for i in $(ls $FOLDER/*.bam); do
	x=${i%.bam} # make the file name
	# make the gonomecov file and sort it by chromosome and starting base
	bedtools genomecov -bg -strand + -ibam $i | awk '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $4, $4 * ($3 - $2), "+")}' > $x$EXTENSION
	bedtools genomecov -bg -strand - -ibam $i | awk '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $4, $4 * ($3 - $2), "-")}' >> $x$EXTENSION
	sort -k 1,1 -k2,2n $x.bed > ${x}_sorted$EXTENSION # this file is a graph like representation of a bed file
	rm $x.bed # delete the unsorted file	
	bedtools merge -s -d $JUMP -c 5 -o sum -i ${x}_sorted$EXTENSION | awk -v var="$x" '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, var, $5, $4)}' >> $FOLDER/$OUTPUT
done

# sort the global file in order to use merge on it
sort -k 1,1 -k2,2n $FOLDER/$OUTPUT > $FOLDER/sorted_$OUTPUT # before merge
# TODO add or remove the "-d $JUMP" ? example V:6146-7537
bedtools merge -d $JUMP -s -i $FOLDER/sorted_$OUTPUT | awk '{printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $3 - $2, $4, $4)}' > $FOLDER/$OUTPUT # this are the global windows 

echo "Done making BED files"
