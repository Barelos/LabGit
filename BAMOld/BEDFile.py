from Sequence import Sequence
class BEDFile:
    # vars for reading the bed file
    _path = None
    _pos_lines = []
    _neg_lines = []
    # vars for depth calculations
    _pos_depth = {}
    _neg_depth = {}
    CHR = 0
    STR = 1
    END = 2
    UMI = 3
    SCR = 4
    # vars for sequence calculations
    _pos_seq = {}
    _neg_seq = {}
    # vars for writing BED file
    BED = "%s\t%s\t%s\t%s\t%s\t%s\n"

    def __init__(self, path):
        self._path = path
        self.read_lines()
        self.calculate_depth()
        self.calculate_seq()
        self.make_bed()

        # self.test_output()

    def read_lines(self):
        with open(self._path, "r") as f:
            for line in f:
                line = line.replace("\n", "").split("\t")
                if line[-1] is "-":
                    self._neg_lines.append(line)
                else:
                    self._pos_lines.append(line)

    def calculate_depth(self):
        # calculate the positive depth and the negative depth
        self._depth(self._pos_lines, self._pos_depth)
        self._depth(self._neg_lines, self._neg_depth)

    def old_calculate_depth(self):
        # calculate pos depth
        for line in self._pos_lines:
            chr = line[self.CHR]
            start = line[self.STR]
            end = line[self.END]
            if chr not in self._pos_depth.keys():
                self._pos_depth[chr] = {}
            for i in range(int(start), int(end) + 1):
                if i not in self._pos_depth[chr].keys():
                    self._pos_depth[chr][i] = 0
                self._pos_depth[chr][i] += 1
        # calculate neg depth
        for line in self._neg_lines:
            chr = line[self.CHR]
            start = line[self.STR]
            end = line[self.END]
            if chr not in self._neg_depth.keys():
                self._neg_depth[chr] = {}
            for i in range(start, end + 1):
                if i not in self._neg_depth[chr].keys():
                    self._neg_depth[chr][i] = 0
                self._neg_depth[chr][i] += 1

    def _depth(self, lines, depth):
        # calculate pos depth
        for line in lines:
            chr = line[self.CHR]
            start = line[self.STR]
            end = line[self.END]
            if chr not in depth.keys():
                depth[chr] = {}
            for i in range(int(start), int(end) + 1):
                if i not in depth[chr].keys():
                    depth[chr][i] = 0
                depth[chr][i] += 1

    def calculate_seq(self):
        self._seq(self._pos_depth, self._pos_seq)
        self._seq(self._neg_depth, self._neg_seq)

    def _seq(self, depth, seq):
        # calculate positive sequences
        for chr in depth.keys():
            seq[chr] = []
            keys = list(depth[chr].keys())
            keys = sorted(keys)
            seq_depth = [depth[chr][keys[0]]] # add the depth of the first base
            cur_start = keys[0]
            last = keys[0]
            for i in range(1, len(keys)):
                if keys[i] - last > 1:
                    seq[chr].append(Sequence(chr, cur_start, last, seq_depth))
                    cur_start = keys[i]
                    last = keys[i]
                    seq_depth = [depth[chr][keys[i]]]
                else:
                    seq_depth.append(depth[chr][last])
                    last = keys[i]

    def make_bed(self):
        output_name = self._path.replace(".txt", ".bed")
        f = open(output_name, "w")
        self._write_seq(self._pos_seq, f, "+")
        self._write_seq(self._neg_seq, f, "-")
        f.close()

    def _write_seq(self, seq, f, sign):
        pos_or_neg = "POS" if sign is "+" else "NEG"
        for chr in seq.keys():
            for s in seq[chr]:
                f.write(self.BED % (s.chr, s.start, s.end, pos_or_neg, s.total_depth, sign))

    def test_output(self):
        user_input = input()
        pos = 0
        neg = 0
        while user_input is not "q":
            if user_input is "-":
                print(self._neg_lines[neg])
                neg += 1
                user_input = input()
            elif user_input is "+":
                print(self._pos_lines[pos])
                pos += 1
                user_input = input()
            elif user_input is "q":
                break
            else:
                user_input = input("input is only: +/-/q")