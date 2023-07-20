from scipy.special import hyp2f1
from scipy.interpolate import interp1d
import numpy as np
from params import *
import pandas as pd


def get_sr(rp_max, iter=0):
    """
    calculate core length depends on radius of the balloon
    using scipy.special package's funtction: 
    - hyp2f1: 2F1 hypergeometric function
    
    :param rp_max: maximal radius of the balloon (pumpkin shape)
    :return: list of radii and list of core lengths
    """
    if iter==0:
        r_list = np.linspace(0, rp_max, int(rp_max / 0.002))
    else:
        r_list = rp_max
        rp_max = max(r_list)

    s_list = []

    for r in r_list:
        # equation for calculating s0
        s = r * hyp2f1(1 / 4, 1 / 2, 5 / 4, (r / rp_max) ** 4)
        s_list.append(s)
    return r_list, s_list


def interpolate(s_half, s_input, r, iter=0):
    """
    interpolate core length depends on radius of the balloon
    using scipy.special package's funtction: 
    - hyp2f1: 2F1 hypergeometric function
    and scipy.interpolate package's function:
    - interp1d: interpolate a 1-D function
    
    :param s_half: interpolation points (half of them, at the rest will be symmetrical)
    :r: radii at these values of s
    :return: list of radii and list of core lengths
    """
    f = interp1d(s_half, r, kind='cubic')
    s0 = 0
    if iter==0:
        s = np.arange(s0, l + ds, ds)
    else:
        s = s_input

    rp = []
    for i in s[:-1]:
        if i <= l / 2:
            rp.append(f(i))
        else:
            rp.append(f(l - i))
    return s[:-1], rp


# rs, s_half = get_sr(rp_max) # just gets lists of s and r for half of the balloon's core length
# s, rp = interpolate(s_half, 0, rs)
# d = {'s': s, 'rp': rp}
# df = pd.DataFrame(data=d)
# df.to_csv("rp_s_002_new.csv")

# rs = rp[0:len(rp)//2]
# rs_new, s_half_new = get_sr(rs, 1)
# s_new, rp_new = interpolate(s_half_new, s, rs_new, 1)
# d_upd = {'s': s_new, 'rp': rp_new}
# df_upd = pd.DataFrame(data=d_upd)
# df_upd.to_csv("rp_s_002_updated.csv")