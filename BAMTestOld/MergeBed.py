from os import listdir
from os.path import isfile, join

import sys


def get_file_names(file_path):
    if file_path.endswith("/"):
        file_path = file_path[:-1]

    only_bed = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    only_bed = [f for f in only_bed if f.endswith(".bed")]

    return only_bed


def merge(bam_files):
    # we make a new output file
    f = open(sys.argv[2], "w")
    # we copy the content of each bam file to one long bam file
    for file in bam_files:
        with open(sys.argv[1] + "/" +file, "r") as input:
            for line in input:
                f.write(line)
    f.close()


def merge_files():
    files = get_file_names(sys.argv[1])
    merge(files)


if __name__ == '__main__':
    merge_files()
