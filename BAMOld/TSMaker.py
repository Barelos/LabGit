import tkinter as tk
import math

class TSMaker:

    # the file
    _bed_file = None
    _chr = "chrII"
    # tkinter interface
    _root = None
    _canvas = None
    _frame = None
    _hbar = None
    # dimensions
    C_WIDTH = 800
    C_HEIGHT = 400
    t_width = None
    B_WIDTH = 300
    # colors
    C_BG = "white"
    C_GENE = "blue"
    C_POS = "green"
    C_NEG = "red"
    # locations
    H_NEG = 150
    H_POS = 250
    H_GENE = 350
    H_ALL = 50
    # output calculations vars
    result_pos = {}
    result_neg = {}
    locations_pos = None
    locations_neg = None

    def __init__(self, bed_file):
        # we calculate how nuch space we need
        self._bed_file = bed_file
        self.calculate_width()
        # we build the window
        self._root = tk.Tk()
        self._frame = tk.Frame(self._root, width=self.C_WIDTH, height=self.C_HEIGHT)
        self._frame.grid(row=0, column=0)
        self._canvas = tk.Canvas(self._frame, bg=self.C_BG, width=self.C_WIDTH, height=self.C_HEIGHT, scrollregion=(0,0,self.t_width, self.C_HEIGHT))
        self._hbar = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)
        self._hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self._hbar.config(command=self._canvas.xview)
        self._canvas.config(width=self.C_WIDTH, height=self.C_HEIGHT)
        self._canvas.config(xscrollcommand=self._hbar.set)
        # definition of event handling
        self._canvas.bind("<Button-1>", self.press)
        # we draw and pack the canvas
        self.draw_seq()
        self._canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        # inferstructure for search by location
        self.locations_pos = list(sorted(self.result_pos.keys()))
        self.locations_neg = list(sorted(self.result_neg.keys()))
        # start the main loop
        self._root.mainloop()

    def press(self, event):
        if self.H_POS <= event.y <= self.H_POS + self.H_ALL:
            seq = self.find_closest(self.locations_pos, event.x)
        elif self.H_NEG <= event.y <= self.H_NEG + self.H_ALL:
            seq = self.find_closest(self.locations_neg, event.x)
        else:
            return

        if seq is None:
            print("OOPS!?!?!")
            return
        seq.is_gene = not seq.is_gene
        self._canvas.delete(seq.ref)
        color = self.C_POS if seq.is_gene else self.C_NEG
        seq.ref = self._draw_shape(seq, seq.sign, color)

    # TODO test logic of search because it does not work!!!!!
    def find_closest(self, locations, x):
        left_bound = 0
        right_bound = len(locations)
        mid = int(right_bound / 2)
        index = None
        found = False
        while not found:
            # should we look left or right?
            if x < locations[mid]:
                # am i the closest?
                if x >= locations[mid - 1]:
                    index =  locations[mid - 1]
                    found = True
                else:
                    right_bound = mid - 1
                    mid = left_bound + int((right_bound - left_bound) / 2)
            elif x > locations[mid]:
                # am i the closest?
                if x <= locations[mid + 1]:
                    index = locations[mid + 1]
                    found = True
                else:
                    left_bound = mid + 1
                    mid = left_bound + int((right_bound - left_bound) / 2)
            else:
                index =  x
                found = True

        seq = self.result_pos[index] if locations is self.locations_pos else self.result_neg[index]
        if x >= seq.start:
            return seq
        else:
            return None

    def calculate_width(self):
        max_pos = self._bed_file._pos_seq[self._chr][-1].end
        max_neg = self._bed_file._neg_seq[self._chr][-1].end
        self.t_width = max(max_pos, max_neg)

    def draw_seq(self):
        self._draw(self._bed_file._pos_seq[self._chr], "+")
        self._draw(self._bed_file._neg_seq[self._chr], "-")

    def _draw(self, seq_list, sign):
        for seq in seq_list:
            seq.ref = self._draw_shape(seq, sign, self.C_NEG)
            seq.sign = sign
            if sign is "+":
                self.result_pos[seq.end] = seq
            else:
                self.result_neg[seq.end] = seq

    def _draw_shape(self, seq, sign, color):
        height = self.H_POS if sign is "+" else self.H_NEG
        if sign is "+":
            return self._canvas.create_polygon(seq.start, height, seq.end, height,
                                               seq.end + self.H_ALL / 2, height + self.H_ALL / 2,
                                               seq.end, height + self.H_ALL, seq.start, height + self.H_ALL,
                                               fill=color)
        else:
            return self._canvas.create_polygon(seq.start, height, seq.end, height,
                                               seq.end, height + self.H_ALL, seq.start, height + self.H_ALL,
                                               seq.start - self.H_ALL / 2, height + self.H_ALL / 2,
                                               fill=color)