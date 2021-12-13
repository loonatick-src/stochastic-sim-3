class CoolingSchedule:
    def __init__(self, func, *args):
        self.f = func
        self.args = args

    def __call__(self, T):
        return self.f(T, *self.args)


class GeometricCoolingSchedule(CoolingSchedule):
    def __init__(self, cr):
        self.args = (None,)
        self.f = lambda T, _: cr * T
