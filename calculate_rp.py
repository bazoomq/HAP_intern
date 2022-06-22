from scipy.special import hyp2f1
from scipy.interpolate import interp1d
import numpy as np


def get_sr(rp_max):
    r_list = np.linspace(0, rp_max, int(rp_max / 0.001))
    s_list = []

    for r in r_list:
        # equation for calculating S0
        s = r * hyp2f1(1 / 4, 1 / 2, 5 / 4, (r / rp_max) ** 4)
        s_list.append(s)
    return r_list, s_list


def interpolate(s_half, r, rp_max):
    f = interp1d(s_half, r, kind='cubic')
    s0 = 0
    l = 2 * rp_max * hyp2f1(1 / 4, 1 / 2, 5 / 4, 1)
    ds = 0.002
    s = np.arange(s0, l + ds, ds)
    rp = []
    for i in s[:-1]:
        if i <= l / 2:
            rp.append(f(i))
        else:
            rp.append(f(l - i))
    return s[:-1], rp
