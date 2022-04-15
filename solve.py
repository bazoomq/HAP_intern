import numpy as np
from RK import OneStepMethod, RungeKuttaMethod
from ODE import NaturalShapeEq
import coeffs
from density import density


def integration(method: OneStepMethod, func, y_start, ts):
    """
    performs fix-step integration using one-step method
    ts: array of timestamps
    return: list of t's, list of y's
    """
    ys = [y_start]

    for i, t in enumerate(ts[:-1]):
        y = ys[-1]

        y1 = method.step(func, t, y, ts[i + 1] - t)
        ys.append(y1)

    return ts, ys


def one_step(theta0):
    h = 4000
    L0 = 9.8
    w = 0.2254
    z0 = 0
    s0 = 0
    r0 = 0
    y0 = np.array([theta0, L0 / np.cos(theta0), z0, r0])
    rp = 6
    s1 = 2.62 * rp
    ds = 0.1
    ro_atm = density(h)[0]
    ro_gas = density(h)[1]
    f = NaturalShapeEq(y0, ro_atm, ro_gas, w)
    s = np.arange(s0, s1 + ds, ds)

    f.clear_call_counter()
    _, y = integration(RungeKuttaMethod(coeffs.rk4_coeffs), f, y0, s)
    n_calls = f.get_call_counter()
    print(f'One-step {RungeKuttaMethod(coeffs.rk4_coeffs)}: {len(y)-1} steps, {n_calls} function calls')
    #return [i[0] for i in y], [i[1] for i in y], [i[2] for i in y], [i[3] for i in y]
    return np.array(y)[:, 0], np.array(y)[:, 1], np.array(y)[:, 2], np.array(y)[:, 3]

'''
if __name__ == "__main__":
    one_step(0.5)
'''


