from os import listdir
from os.path import isfile, join
from BEDFile import BEDFile
from TSMaker import TSMaker
directory = "input"
files = []


def main():
    only_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith(".txt")]
    for f in only_files:
        files.append(BEDFile(directory + "/" + f))
    TSMaker(files[0])

main()