from polyline import Polyline
import paterns
class BoxPatern:
    def __init__(self, cut, fold, in_mark_rec, ex_mark_rec, **box_info):
        self.cut: list[Polyline] = []
        self.fold: list[Polyline] = []
        self.ex_mark_rec: list[Polyline] = []
        self.in_mark_rec: list[Polyline] = []
        self.template = True
        self.multiplyers = set()
        self.size = None

        for cu in cut:
            self.cut.append(Polyline(*cu[0], closed=cu[1], side=cu[2]))
        for fo in fold:
            self.fold.append(Polyline(*fo[0], closed=fo[1], side=fo[2]))
        for i in in_mark_rec:
            self.in_mark_rec.append(Polyline(*i[0], closed=i[1], side=i[2]))
        for ex in ex_mark_rec:
            self.ex_mark_rec.append(Polyline(*ex[0], closed=ex[1], side=ex[2]))

    def calculate_box(self, **multiplyers: dict[str, float]):
        self.cut = list(map(lambda x: x.calculate(**multiplyers), self.cut))
        self.fold = list(map(lambda x: x.calculate(**multiplyers), self.fold))
        self.in_mark_rec = list(map(lambda x: x.calculate(**multiplyers), self.in_mark_rec))
        self.ex_mark_rec = list(map(lambda x: x.calculate(**multiplyers), self.ex_mark_rec))
        x_all, y_all = [], []
        for c in self.cut:
            u, v = zip(*c.vertices)
            x_all.extend(u)
            y_all.extend(v)
        self.size = (max(x_all)-min(x_all), max(y_all)-min(y_all))
        self.template = False
