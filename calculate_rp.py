from scipy.special import hyp2f1
from scipy.interpolate import interp1d
import numpy as np
from params import *


def get_sr(rp_max):
    """
    calculate core length depends on radius of the balloon
    using scipy.special package's funtction: 
    - hyp2f1: 2F1 hypergeometric function
    
    :param rp_max: maximal radius of the balloon (pumpkin shape)
    :return: list of radii and list of core lengths
    """
    r_list = np.linspace(0, rp_max, int(rp_max / ds))
    s_list = []

    for r in r_list:
        # equation for calculating s0
        s = r * hyp2f1(1 / 4, 1 / 2, 5 / 4, (r / rp_max) ** 4)
        s_list.append(s)
    return r_list, s_list


def interpolate(s_half, r):
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
    s = np.arange(s0, l + ds, ds)
    
    rp = []
    for i in s[:-1]:
        if i <= l / 2:
            rp.append(f(i))
        else:
            rp.append(f(l - i))
    return s[:-1], rp
