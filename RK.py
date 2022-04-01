import numpy as np
from ODE import ODE
from coeffs import RKScheme


class OneStepMethod:
    def __init__(self, **kwargs):
        self.name = 'default_method'
        self.p = None
        self.__dict__.update(**kwargs)

    def step(self, func: ODE, t, y, dt):
        """
        make a step: t => t+dt
        """
        return t + dt


class RungeKuttaMethod(OneStepMethod):
    """
    Explicit Runge-Kutta method with (A, b) coefficients
    """
    def __init__(self, coeffs: RKScheme):
        super().__init__(**coeffs.__dict__)

    def step(self, func: ODE, t, y, dt):
        A = self.A
        b = self.b
        n = np.size(b)
        c = np.sum(A, axis=1)
        k = np.zeros((n, len(y)))
        for i in range(n):
            k[i] = np.array(dt * func(t + dt * c[i], y + np.dot(A[i], k)))
        res = y + b.dot(k)
        return res

