import sys
from genericpath import isfile
from os import listdir
from os.path import join
from Constants import *
import matplotlib.pyplot as plt

AND = False
NUM_FILES = None


def add_key(key, val, dictionary):
    if key not in dictionary.keys():
        dictionary[key] = val


def get_name(path):
    names = path.split("/")
    return names[-1].replace(".bam", "")


def get_file_names(file_path):
    if file_path.endswith("/"):
        file_path = file_path[:-1]

    only_bed = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    only_bed = [f for f in only_bed if f.endswith(".bed")]

    return only_bed


def read_lines(path=None):
    """
    make a list of lines
    :return:
    """
    pos_lines = []
    neg_lines = []
    if path is not None:
        with open(path) as f:
            for line in f:
                if line.endswith("+\n"):
                    pos_lines.append(line)
                else:
                    neg_lines.append(line)
    else:
        for line in sys.stdin:
            if line.endswith("+\n"):
                pos_lines.append(line)
            else:
                neg_lines.append(line)
    return pos_lines, neg_lines


def find_depth(lines):
    """
    find the number of reads pe base
    :param lines:
    :return:
    """
    # we make a pos depth and neg depth
    solution = {}
    for line in lines:
        # we get the data we want
        data = line.split("\t")
        chromosome = data[CHR]
        start = data[START]
        end = data[END]
        # we make a new chromosome holder if we need to
        add_key(chromosome, {}, solution)
        # we add 1 to the count per base in the read
        for i in range(int(start), int(end) + 1):
            # add the key if needed
            add_key(i, 0, solution[chromosome])
            # add 1
            solution[chromosome][i] += 1

    # we return the pos and neg depth
    return solution


def threshold_depth(depth_list):
    out = []
    for key in depth_list.keys():
        for inkey in depth_list[key].keys():
            if depth_list[key][inkey] < int(NUM_FILES):
                out.append((key, inkey))
    for name in out:
        depth_list[name[0]].pop(name[1], None)

    return depth_list


def find_seq(input_seq):
    solution = {}
    # we find the depth for each chromosome
    for key in input_seq.keys():
        solution[key] = list()
        # we sort the bases that we found from the chromosme
        bases = input_seq[key].keys()
        bases = sorted(bases)
        # we make a counter and start pointer
        start = 0
        count = 0
        num_reads = 0
        # we go base by base and test if he is a parrt of a sequence
        for i in range(len(bases) - 1):
            if bases[i + 1] - bases[i] > 1:
                solution[key].append([bases[start], bases[start + count], count + 1, num_reads])
                start = i + 1
                count = 0
                num_reads = 0
            else:
                count += 1
                num_reads += input_seq[key][bases[i]]
    # return the solution
    return solution


def make_bed(pos_seq, neg_seq):
    # open a file to write to
    name = get_name(sys.argv[2])
    f = open(sys.argv[1] + "/output%s.bed" % name, "w")
    # add all the positive sequences
    for key in pos_seq.keys():
        for seq in pos_seq[key]:
            f.write(BED % (key, seq[0], seq[1], "POS", str(seq[1] - seq[0]), "+"))
    # add all the negative sequences
    for key in neg_seq.keys():
        for seq in neg_seq[key]:
            f.write(BED % (key, seq[0], seq[1], "NEG", str(seq[1] - seq[0]), "-"))
    # close the file writer
    print("Finished with file %s" % name)
    f.close()


def plot_data(data_pos, data_neg):

    plt.xlabel("length")
    plt.ylabel("num of reads")
    plt.title("Length to Reads")

    for key in data_pos.keys():
        for data in data_pos[key]:
            plt.plot(data[2], data[3])

    for key in data_neg.keys():
        for data in data_neg[key]:
            plt.scatter(data[2], data[3])
    plt.savefig(sys.argv[1] +"/graph_%s.png" % get_name(sys.argv[2]))


def main():
    # we set the running type based on user input
    global AND
    global NUM_FILES
    path = None
    if len(sys.argv) == 6:
        path = sys.argv[3]
        if sys.argv[4] == "AND":
            AND = True
        NUM_FILES = sys.argv[5]
    # get the file and read it
    pos_lines, neg_lines = read_lines(path)
    # make a pos depth and negative depth
    pos = find_depth(pos_lines)
    neg = find_depth(neg_lines)
    # we threshold the depth if needed
    if AND:
        print("Thresholding based on number of files")
        pos = threshold_depth(pos)
        neg = threshold_depth(neg)
    # make list of pos sequences and negative sequences
    pos_seq = find_seq(pos)
    neg_seq = find_seq(neg)
    # make a bed file
    make_bed(pos_seq, neg_seq)
    # show the plot of the data
    plot_data(pos_seq, neg_seq)

if __name__ == '__main__':
    main()
