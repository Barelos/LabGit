import sys

# CONSTANTS
CHR = 0
START = 1
END = 2
COUNT = 3
LEN = 4
STRAND = 5

NUM_FEATURES = 6

FOLDER = 1
NAME = 2
NUM_BED = 3

# GLOBAL VARS
windows = []

def get_total(window, index):
	total = 0	
	for i in range(int(sys.argv[NUM_BED])):
		total += int(window[index + NUM_FEATURES * i])
	return total

def main():
	INTERSECTION = int(sys.argv[NUM_BED]) * NUM_FEATURES # calculate the inedx of the <intersection len> column 
	# go iterate the windows
	with open(sys.argv[FOLDER] + "/" + sys.argv[NAME]	) as f:
		for window in f.readlines():	
			window = window.replace("\n", "").split("\t")						
			# calculate features of a window
			total_fetures = (get_total(window, COUNT), get_total(window, LEN), int(window[INTERSECTION]))
			# TODO add here a frame work to manualy sort "noise" from "real" windows and output to a trainig set file
			# TODO sort automaticly based on learned data
			# TODO update the global windows file to present the features of "real" windows and remove noise windows

if __name__=='__main__':
	main()
