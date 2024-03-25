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
                ((0,), ('-x', '-z', '-t'))
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
                (("x", "y", "1.5t"), ("0.5x", "0.5t")),
                ((0,), ("z",))
            ],
            False,
            0
        ),
        (
            [
                (("2x", "y", "2.5t"), ("z", "0.5x", "0.5t")),
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



