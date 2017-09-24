import sys

# the format is <chromosome> <start> <end> <count> <length> <strand>
WINDOW_FORMAT = "{}\t{}\t{}\t{}\t{}\t{}\n" # if more info is needed change format and write function
# index in BED file
CHR = 0
START = 1
END = 2
COUNT = 3
# index in input
FILE_NAME = 1
SUFFIX = 2
STRAND = 3
JUMP = 4

def write_to_file(file, chrom, start, end, count, jump,  strand):
	file.write(WINDOW_FORMAT.format(chrom, start + jump, end - jump, count, end - start - 2 * jump, strand))

def main():
	jump = int(sys.argv[JUMP])
	# open file to write windows to
	f= open(sys.argv[FILE_NAME] + sys.argv[SUFFIX], 'a+')
	# get the first window start	
	first = sys.stdin.readline().replace("\n", "").split("\t") # the first line in the file
	start = int(first[START]) # start of a window
	end = int(first[END]) # candidate for end of window
	chrom = first[CHR] # which chromosome this window belongs to
	count = (end - start - 2 * jump) * int(first[COUNT])
	strand = sys.argv[STRAND]
	# go line by line and calculate a window based on big jumps
	for line in sys.stdin:
		line = line.split("\t")
		# if a new window is found save it to a file
		if int(line[START]) > end or chrom != line[CHR]:
			# write the window
			write_to_file(f, chrom, start, end, count, jump, strand)
			# initiate a new window			
			start = int(line[START])
			chrom = line[CHR]
			count = 0
		# update end candidate and count			
		end = int(line[END])
		count += (end - int(line[START]) - 2 * jump) * int(line[COUNT])

	#write last window
	write_to_file(f, chrom, start, end, count, jump, strand)
	# close the file in the end
	f.close()	

# run the main function on execution
if __name__ == '__main__':
	main()
