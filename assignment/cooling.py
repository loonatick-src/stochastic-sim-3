import unittest

class CoolingSchedule:
    def __init__(self, func, *args):
        self.f = func
        self.args = args

    def __call__(self, T, *args):
        return self.f(T, *self.args, *args)


class GeometricCoolingSchedule(CoolingSchedule):
    def __init__(self, cr):
        self.args = (None,)
        self.f = lambda T, _, k: T * cr**k

class CoolingTestMethods(unittest.TestCase):
    def test_geometric(self):
        T0 = 100.0
        c = 0.9
        cooling_schedule = GeometricCoolingSchedule(c)
        T_lag = T0
        for i in range(1,10):
            T = cooling_schedule(T0, i)
            self.assertTrue(abs(T - c * T_lag) <= 1.0e-6)
            T_lag = T


if __name__ == '__main__':
    unittest.main()
