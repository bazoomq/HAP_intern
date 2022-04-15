import numpy as np
from utils import call_counter


class ODE:
    """
    y0 = [theta0, T0, z0, r0]
    y = [theta, T, z, r]
    """
    def __init__(self, y0):
        self.y0 = y0

    def __call__(self, s, y):
        raise NotImplementedError


class NaturalShapeEq(ODE):
    """
    theta' = (-2 * pi * r * w * sin(theta) + p) / T
    T' = 2 * pi * r * w * cos(theta)
    z' = cos(theta)
    r' = sin(theta)
    """

    def __init__(self, y0, ro_atm, ro_gas, w):
        self.ro_atm = ro_atm
        self.ro_gas = ro_gas
        self.w = w
        super().__init__(y0)

    @call_counter
    def __call__(self, s, y, g=9.8):
        theta = (-2 * np.pi * y[3] * (self.w * np.sin(y[0]) +
                 g * (self.ro_atm - self.ro_gas) * y[2])) / y[1]
        T = 2 * np.pi * y[3] * self.w * np.cos(y[0])
        z = np.cos(y[0])
        r = np.sin(y[0])
        return np.array([theta, T, z, r])

    def get_call_counter(self):
        return self.__call__.calls

    def clear_call_counter(self):
        self.__call__.__dict__['calls'] = 0
