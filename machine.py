#enviroment describes limitations and parameters of machine used when cuttin material.
from polyline import Polyline
class Machine:
    def __init__(self, machine_type, size_x, size_y, config, post):
        self.machine_type = machine_type
        self.size_x = size_x
        self.size_y = size_y
        self.config = config
        self.post = post
        self.work_area = [Polyline(*[
            ((0,), (0,)),
            ((self.size_x,), (0,)),
            ((0,), (self.size_y,)),
            ((-self.size_x,), (0,)),
            ((0,), (-self.size_y,))
        ], closed=True, side=0)]
