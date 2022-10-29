import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from density import density
from calculate_rp import get_sr
from params import *


def b(h):
    ro_atm = density(h)[0][0]
    ro_gas = density(h)[0][1]
    b = (ro_atm - ro_gas) * g
    return b


rs, s_half = get_sr(rp_max)
f = interp1d(s_half, rs, kind='cubic')


def Solve(params, rmax, velocity):
    def func(t, y):
        if t <= l / 2:
            rp = f(t)
        else:
            rp = f(l - t)
        theta, T, z, r = y
        
        p = b(h) * (z - params[1])
        sin = np.sin(theta)
        cos = np.cos(theta)
        return [
            - 2 * np.pi * (rp * wp * sin + p * r) / T,
            2 * np.pi * rp * wp * cos,
            cos,
            sin
        ]
    
    z0, r0 = 0, 0
    T0 = (L0 + Cx * density(h)[0][0] * velocity * abs(velocity) * math.pi * rmax**2 / 2) / np.cos(params[0])

    sol = solve_ivp(func, t_span=[0, l], y0=[params[0], T0, z0, r0], t_eval=np.arange(0, l, ds))

    return sol.y
