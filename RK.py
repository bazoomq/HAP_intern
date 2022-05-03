import numpy as np
from ODE import ODE
from coeffs import RKScheme
from scipy.integrate import RK45
from scipy.optimize import fsolve


class OneStepMethod:
    def __init__(self, **kwargs):
        self.name = 'default_method'
        self.p = None
        self.__dict__.update(**kwargs)

    def step(self, func: ODE, s, y, ds):
        """
        make a step: s => s+ds
        """
        return s + ds


class ExplicitEulerMethod(OneStepMethod):
    """
    Explicit Euler method (no need to modify)
    order is 1
    """
    def __init__(self):
        super().__init__(name='Euler (explicit)', p=1)

    def step(self, func: ODE, s, y, ds):
        return y + ds * func(s, y)

'''
class RungeKuttaMethod(OneStepMethod):
    """
    Явный метод Рунге-Кутты с коэффициентами (A, b)
    Замените метод step() так, чтобы он не использовал встроенный класс RK45
    """
    def __init__(self, coeffs: RKScheme):
        super().__init__(**coeffs.__dict__)

    def step(self, func: ODE, s, y, ds):
        A, b = self.A, self.b
        rk = RK45(func, s, y, s + ds)
        rk.h_abs = ds
        rk.step()
        return rk.y
'''


class RungeKuttaMethod(OneStepMethod):
    """
    Explicit Runge-Kutta method with (A, b) coefficients
    """
    def __init__(self, coeffs: RKScheme):
        super().__init__(**coeffs.__dict__)

    def step(self, func: ODE, s, y, ds):
        A = self.A
        b = self.b
        n = np.size(b)
        c = np.sum(A, axis=1)
        k = np.zeros((n, len(y)))
        for i in range(n):
            k[i] = np.array(func(s + ds * c[i], y + ds * np.dot(A[i], k)))
        res = y + ds * b.dot(k)
        return res

