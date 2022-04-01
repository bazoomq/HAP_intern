import numpy as np


class RKScheme:
    """
    Runge-Kutta scheme (A,b) of order p
    """
    def __init__(self, name, A, b, p):
        self.name = name
        self.A = np.array(A)
        self.b = np.array(b)
        self.p = p


rk4_coeffs = RKScheme(
    name='RK4',
    A=[
        [0.0, 0.0, 0.0, 0.],
        [0.5, 0.0, 0.0, 0.],
        [0.0, 0.5, 0.0, 0.],
        [0.0, 0.0, 1.0, 0.],
    ],
    b=np.array([1, 2, 2, 1]) / 6,
    p=4,
)