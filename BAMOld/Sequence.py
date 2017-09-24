
class Sequence:

    # base vars
    chr = None
    start = None
    end = None
    depth = None
    # calculations vars
    total_depth = None
    expected_value = None
    variance = None
    peak = None
    # vars used in making the training set
    ref = None
    is_gene = False
    sign = None

    def __init__(self, chr, start, end, depth):
        self.chr = chr
        self.start = start
        self.end = end
        self.depth = depth
        self.calculations()

    def calculations(self):
        self.total_depth = sum(self.depth)
        self.expected_value = self.total_depth / len(self.depth)
        self._variance()
        self.peak = max(self.depth)

    def _variance(self):
        ev_squared = sum(map(lambda x:x*x, self.depth)) / len(self.depth)
        self.variance = ev_squared - self.expected_value * self.expected_value