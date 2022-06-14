
import numpy as np
from scipy.special import hyp2f1
from scipy.interpolate import interp1d
from constants import rp_max

r_list = np.linspace(0, rp_max, int(rp_max/0.001))
s_list = []

for r in r_list:
  # equation for calculating S0
  s = r * hyp2f1(1 / 4, 1 / 2, 5 / 4, (r / rp_max) ** 4)
  s_list.append(s)

def f_interp1d(t):
    rs, s_half = r_list, s_list
    f = interp1d(s_half, rs, kind='cubic')
    return f(t)