import pandas as pd
from scipy.special import hyp2f1
from scipy.interpolate import interp1d
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

#sol = solve_ivp(f, t_span=[0, s1], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, s1, ds))


def get_sr(rp_max):
    r_list = np.linspace(0, rp_max, int(rp_max/0.001))
    s_list = []

    for r in r_list:
        # equation for calculating S0
        s = r * hyp2f1(1 / 4, 1 / 2, 5 / 4, (r / rp_max) ** 4)
        s_list.append(s)
    return r_list, s_list


def interpolate(s_half, r, rp_max):
    f = interp1d(s_half, r, kind='cubic')
    s0 = 0
    s1 = 2 * rp_max * hyp2f1(1 / 4, 1 / 2, 5 / 4, 1)
    ds = 0.002
    s = np.arange(s0, s1 + ds, ds)
    rp = []
    rp_f = []
    for i in s[:-1]:
        if i <= s1 / 2:
            rp.append(f(i))
        else:
            rp.append(f(s1 - i))
    return s[:-1], rp



'''
rp_max = 6.122831
r, s_half = get_sr(rp_max)


plt.plot(s_half, r, '.', interpolate(s_half, r, rp_max)[0], interpolate(s_half, r, rp_max)[1])
plt.legend(['data', 'cubic'], loc='best')
plt.show()

import pandas as pd
s = interpolate(s_half, r, rp_max)[0]
rp = interpolate(s_half, r, rp_max)[1]
sdf = pd.DataFrame(s, columns=['s'])
rpdf = pd.DataFrame(rp, columns=['rp'])
gt = pd.concat([sdf, rpdf], axis=1)
gt = gt.set_index('s')
'''
#gt.to_excel('s_rp.xlsx')
#print(float(gt.loc[16.046]))

