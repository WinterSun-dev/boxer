import functools
import itertools

"""
box_info is dictionary:
    cut: list of Polylines
    fold: list of Polylines
    in_mark: list of rectangles to locate internal markings
    ex_mark: list of rectangles to locate external markings

Polyline is tuple of vectors, is closed, side:
    ( [ ((aX, bY, cZ, dT, e), (aX, bY, cZ, dT, e)), vec, vec, ... ], False, 1)

    triangle hole, 15 + material thickness from edges:
        ([(('t', 15),('t', 15)), (('30x',), (0,)), (('-30x',),('40y',))], True, 2)

    0 terms can be left out, but total 0 must exist
    case-insensitive
    a ... d are constant multipliers
    X, Y, Z : box internal dimensions multipliers
    T : material thickness multiplier
    e : Constant

    By default, Polyline is open (closed = False)
    First vector in polyline is relative point from origin
    Side is integer (0, 1, 2) that represents side where tool cuts using tool offset:
        0 = center
        1 = right
        2 = left


rectangle is 4 segment polyline:
    rectangle vertices relative to marking orientation in order:
        bottom - right
        top    - right
        top    - left
        bottom - left
    default order of edges is also right -> top -> left -> bottom
    (see. radians for more info)

Internal and external refer contex of user not sides of box:
    internal: "DB_123_s_45"
    external: "Developer Boots"

"""

basic_box_patern = {
    "cut": [
        (
            [
                ((0,), (0,)),
                (("x",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("t",), (0,)),
                ((0,), ("-0.5x", "-0.5t")),
                (("y",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("t",), (0,)),
                ((0,), ("-0.5x", "-0.5t")),
                (("x",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("t",), (0,)),
                ((0,), ("-0.5x", "-0.5t")),
                (("y",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("0.5t", 20), (0,)),
                ((0,), ("z",)),
                (("-0.5t", -20), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("-y",), (0,)),
                ((0,), ("-0.5x", "-0.5t")),
                (("-t",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("-x",), (0,)),
                ((0,), ("-0.5x", "-0.5t")),
                (("-t",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("-y",), (0,)),
                ((0,), ("-0.5x", "-0.5t")),
                (("-t",), (0,)),
                ((0,), ("0.5x", "0.5t")),
                (("-x",), (0,)),
            ],
            True,
            1
        ),
    ],
    "fold": [
        (
            [
                ((0,), ("0.5x",)),
                (("2x", "2y", "3t"), (0,)),
                ((0,), ("z", "t")),
                (("-2x", "-2y", "-3t"), (0,)),

            ],
            False,
            0
        ),
        (
            [
                (("x", "0.5t"), ("z", "0.5x", "0.5t")),
                ((0,), ("-z",))
            ],
            False,
            0
        ),
        (
            [
                (("x", "y", "t"), ("0.5x", "0.5t")),
                ((0,), ("z",))
            ],
            False,
            0
        ),
        (
            [
                (("2x", "y", "0.5t"), ("z", "0.5x", "0.5t")),
                ((0,), ("-z",))
            ],
            False,
            0
        )
    ],
    "in_mark_rec": [
        (
            [
                (("2x", "2y", "3.5t", 18), ("0.5x", "0.5t", 2)),
                ((0,), ("z", -4)),
                (("-0.5t", -16), (0,)),
                ((0,), ("-z", 4))
            ],
            True,
            0
        )
    ],
    "ex_mark_rec": [
        (
            [
                (("x", "t", 4), ("0.5x", "z", "t", 4)),
                (("Y", -8), (0,)),
                ((0,), ("0.5x", "0.5t", -8)),
                (("-Y", 8), (0,))
            ],
            True,
            0
        ),
        (
            [
                (("2x", "y", "3t", 4), ("0.5x", "z", "t", 4)),
                (("Y", -8), (0,)),
                ((0,), ("0.5x", "0.5t", -8)),
                (("-Y", 8), (0,))
            ],
            True,
            0
        )
    ]

}


class BoxPatern:
    def __init__(self, cut, fold, in_mark_rec, ex_mark_rec, **box_info):
        self.cut = cut
        self.fold = fold
        self.ex_mark = ex_mark_rec
        self.in_mark = in_mark_rec
        self.template = True
        self.multiplyers = set()

        all_vector_parts = []
        for unit in [self.cut, self.fold, self.ex_mark, self.in_mark]:
            for pol in unit:
                for vec in pol[0]:
                    all_vector_parts.extend(vec[0] + vec[1])
        self.multiplyers = set(map(lambda y: y.upper(),filter(lambda x: not str(x).isdigit() and x not in (".","-", "[", "]", "'", ",", " "), "".join(str(all_vector_parts)))))








    def calculate(self, multiplyers):
        self.template = False

"""
class BoxPatern AAAAAAAAAAAAAAAAAAA:
    def __init__(self, x: float, y: float, z: float, t: float, in_mark="", ex_mark="",
                 **box_info: dict[str, list[tuple[tuple, bool, int]]]):
        self.cut = box_info["cut"]
        self.fold = box_info["fold"]
        self.ex_mark = box_info["ex_mark_rec"]
        self.in_mark = box_info["in_mark_rec"]
        self.cal_cut = []
        self.cal_fold = []
        self.cal_ex_mark = []
        self.cal_in_mark = []
        self.calculate_polylines(x, y, z, t, self.cut, self.cal_cut)
        self.calculate_polylines(x, y, z, t, self.fold, self.cal_fold)
        self.calculate_polylines(x, y, z, t, self.ex_mark, self.cal_ex_mark)
        self.calculate_polylines(x, y, z, t, self.in_mark, self.cal_in_mark)


    def calculate_polylines(self, x, y, z, t, category, new):
        x = x
        y = y
        z = z
        t = t

        def cal_comp(component):
            ret = 0
            for c in component:
                if type(c) in (int, float):
                    ret += c
                    continue
                match c.upper():
                    case "X": ret += x
                    case "Y": ret += y
                    case "Z": ret += z
                    case "T": ret += t

                    case "-X": ret += -x
                    case "-Y": ret += -y
                    case "-Z": ret += -z
                    case "-T": ret += -t
                    case _:
                        match c[-1].upper():
                            case "X": ret += x * float(c[:-1])
                            case "Y": ret += y * float(c[:-1])
                            case "Z": ret += z * float(c[:-1])
                            case "T": ret += t * float(c[:-1])
                            case _: ret += float(c)
            return ret

        for polyline in category:
            calculated = []
            for vectors in polyline[0]:
                calculated.append((cal_comp(vectors[0]), cal_comp(vectors[1])))
            new.append((calculated, polyline[1], polyline[2]))
"""


new_box = BoxPatern(**basic_box_patern)
print(new_box.multiplyers)

