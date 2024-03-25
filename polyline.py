
def to_abs(vec, **mult: dict[str, float]):

    sum_unit = 0

    for term in vec:
        s_term = str(term).upper()
        if s_term[-1] in mult:
            if len(s_term) > 1 and s_term[-2] == "-":
                sum_unit -= (float(s_term[:-2]) if len(s_term) > 2 else 1) * mult[s_term[-1]]
            else: sum_unit += (float(s_term[:-1]) if len(s_term) > 1 else 1) * mult[s_term[-1]]
        else:
            sum_unit += float(term)
    return sum_unit


class Polyline:
    def __init__(self, *vectors, closed=False, side=0):
        self.vectors = vectors
        self.vertices = []
        self.closed = closed
        self.side = side
        self.size = None

        self.uniq_terms = set()

        for x, y in self.vectors:
            all_units = list(x) + list(y)
            self.uniq_terms.update(set(map(lambda a: a.upper(), filter(lambda b: str(b).isalpha(), "".join(str(all_units))))))
        if len(self.uniq_terms) == 0:
            self.calculate()

    def calculate(self, **multiplyers: dict[str, float]):
        self.vertices = [(0, 0)]
        for x, y in self.vectors:
            self.vertices.append((self.vertices[-1][0] + to_abs(x, **multiplyers),
                                  self.vertices[-1][1] + to_abs(y, **multiplyers)))
        self.uniq_terms = {}
        x_dir, y_dir = zip(*self.vertices)
        self.size = ((min(x_dir), min(y_dir)), (max(x_dir), max(y_dir)))
        del self.vertices[0]
        return self

