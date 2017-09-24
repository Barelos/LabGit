#!/bin/bash

FOLDER=$1 # the working directory
JUMP=$2 # how close must two reads be

# iterate through the BAM files and turn them into window files
for i in $(ls $FOLDER/*.bam); do
	x=${i%.bam} # make the file name
	bedtools genomecov -bg -strand + -ibam $i | awk -v jump=$JUMP {'printf("%s\t%s\t%s\t%s\n", $1, $2 - jump, $3 + jump, $4)'} | python3 main.py $x .bed + $JUMP # calculate positive windows
	bedtools genomecov -bg -strand - -ibam $i | awk -v jump=$JUMP {'printf("%s\t%s\t%s\t%s\n", $1, $2 - jump, $3 + jump, $4)'} | python3 main.py $x .bed - $JUMP # calculate negative windows
	awk -v jump=$JUMP {'printf("%s\t%s\t%s\t%s\t%s\t%s\n", $1, $2 + jump, $3 - jump, $4, $5, $6)'} $x.bed > ${x}_final.bed
	rm $x.bed
done

echo "Done making BED files"
