import unittest
import numpy as np

# No, I am not a Java programmer
# I was not sure how complicated the cooling schedules could get
# So, tried to make a generalized API. Varying degrees of success
class CoolingSchedule:
    """
    In its current state, this class creates a cooling schedule that
    calculates the k-th temperature value from the 0-th temperature
    value and the value of k, as opposed to using the recursive
    one-step formulae

    This is because the logarithmic cooling schedule (see
    `LogarithmicCoolingSchedule`) does not permit a simple one-step
    recursion.
    """
    def __init__(self, func, *args):
        self.f = func
        self.args = args

    def __call__(self, T, *args):
        return self.f(T, *self.args, *args)


class GeometricCoolingSchedule(CoolingSchedule):
    """
    T_k = cr**k * T_0
        = cr * T_{k-1}
    """
    def __init__(self, cr):
        assert 0 < cr < 1
        self.args = (None,)
        self.f = lambda T, _, k: T * cr**k


class LinearCoolingSchedule(CoolingSchedule):
    """
    T_k = T0 - k*alpha
        = T_{k-1} - alpha
    We expect this one to be kind of trash
    """
    def __init__(self, alpha):
        self.args = (None,)
        self.f = lambda T, _, k: T - k*alpha


class LogarithmicCoolingSchedule(CoolingSchedule):
    """
    T_k = T_0/(1 + alpha * log(1+k))
        = T_{k-1} * (1 + log(k))/(1 + log(k+1))
    """
    def __init__(self, alpha):
        assert 0 < alpha < 1
        self.args = (None,)
        self.f = lambda T, _, k: T/(1 + alpha * np.log(1+k))


class ExponentialCoolingSchedule(CoolingSchedule):
    """
    T_k = T_0 * exp(-beta * k)
        = T_{k-1} * exp(-beta)
    """
    def __init__(self, beta):
        assert 0 < beta < 1
        self.args = (None,)
        self.f = lambda T, _, k: T * np.exp(-beta * k)


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


    def test_geometric_fail(self):
        c = 1.1
        with self.assertRaises(AssertionError):
            cooling_schedule = GeometricCoolingSchedule(c)



    def test_linear(self):
        T0 = 100.0
        alpha = 1.5
        cooling_schedule = LinearCoolingSchedule(alpha)
        T_lag = T0
        for i in range(1,10):
            T = cooling_schedule(T0, i)
            self.assertTrue(abs(T - T_lag + alpha) < 1.0e-6)
            T_lag = T

    def test_exponential(self):
        T0 = 100.0
        beta = 0.5
        cooling_schedule = ExponentialCoolingSchedule(beta)
        for i in range(1,10):
            T = cooling_schedule(T0, i)
            self.assertEqual(T0 * np.exp(-beta * i), T)

if __name__ == '__main__':
    unittest.main()
