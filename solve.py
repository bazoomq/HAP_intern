import numpy as np
from RK import OneStepMethod, RungeKuttaMethod
from ODE import NaturalShapeEq
import coeffs

# constants and params
d = 25 * 1e-6
ro_p = 920
g = 9.8

R_p = 6
L = 10 * g
r0 = r1 = 0.25
w_p = d * ro_p / g
roa = 0.09
rog = 0.1


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


def test_one_step():
    y0 = np.array([np.pi/2, ])
    t0 = 0
    t1 = np.pi/2
    dt = 0.1
    w = 0.0023
    p = 0.1
    z0 = 0

    f = NaturalShapeEq(y0, w, p)
    ts = np.arange(t0, t1+dt, dt)

    f.clear_call_counter()
    _, y = integration(RungeKuttaMethod(coeffs.rk4_coeffs), f, y0, ts)
    n_calls = f.get_call_counter()
    print(f'One-step {RungeKuttaMethod(coeffs.rk4_coeffs).name}: {len(y)-1} steps, {n_calls} function calls')
