import numpy as np


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

    def __init__(self, y0, w, p):
        self.w = w
        self.p = p # p = bz
        super().__init__(y0)

    def __call__(self, s, y):
        theta = (-2 * np.pi * y[2] * self.w * np.sin(y[0]) + self.p) / y[1]
        T = 2 * np.pi * y[3] * self.w * np.cos(y[0])
        z = np.cos(y[0])
        r = np.sin(y[0])
        return np.array([theta, T, z, r])
