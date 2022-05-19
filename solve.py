import numpy as np
from RK import OneStepMethod, RungeKuttaMethod, ExplicitEulerMethod
from ODE import NaturalShapeEq, ODE
import coeffs
from density import density
from scipy.special import hyp2f1
from calculate_rp import get_sr, interpolate
from scipy.interpolate import interp1d
import pandas as pd


def integration(method: OneStepMethod, func: ODE, y_start, ts):
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


def one_step(theta0, a):
    h = 22020  # h = 22020, theta0 = 54.37
    g = 9.8
    L0 = 24.06031 * g
    w = 0.229158
    z0 = 0
    s0 = 0
    r0 = 0
    y0 = np.array([theta0, L0 / np.cos(theta0), z0, r0])
    rp_max = 6.122831
    s1 = 2 * hyp2f1(1/4, 1/2, 5/4, 1) * rp_max
    ds = 0.002
    ro_atm = density(h)[0]
    ro_gas = density(h)[1]

    s = np.arange(s0, s1 + ds, ds)
    r, s_half = get_sr(rp_max)

    fs = interpolate(s_half, r, rp_max)[0]
    frp = interpolate(s_half, r, rp_max)[1]
    fsdf = pd.DataFrame(fs, columns=['s'])
    frpdf = pd.DataFrame(frp, columns=['rp'])
    gt = pd.concat([fsdf, frpdf], axis=1)

    #rp = get_rp(, gt)

    func = NaturalShapeEq(y0, ro_atm, ro_gas, w, gt, a)
    func.clear_call_counter()
    _, y = integration(RungeKuttaMethod(coeffs.rk4_coeffs), func, y0, s)
    n_calls = func.get_call_counter()
    print(f'One-step {RungeKuttaMethod(coeffs.rk4_coeffs)}: {len(y)-1} steps, {n_calls} function calls')
    return np.array(y)[:, 0], np.array(y)[:, 1], np.array(y)[:, 2], np.array(y)[:, 3]


if __name__ == "__main__":
    one_step(0.5, 0)
